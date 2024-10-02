from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from app.views import  EmployeesViewSet, ProjectsViewSet, UserViewSet
from django.db.models import Q

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from app.views import login, logout_view

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Тестовое описание",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'id', 'first_name', 'last_name']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):  
        queryset = super().get_queryset() #curl -X GET "http://localhost:8000/users/?keyword="
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(username__icontains=keyword)
                | Q(first_name__icontains=keyword)  
            )
        return queryset

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'employees', EmployeesViewSet)
router.register(r'projects', ProjectsViewSet)
router.register(r'users', UserViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('employees/Age/<int:age>/', EmployeesViewSet.as_view({'get': 'filterEmployeesByAge'}), name='employees-age'),
    path('employees/<int:pk>/newProject/', EmployeesViewSet.as_view({'post': 'newProject'}), name='employees-new-project'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    # path('auth/', include('social_django.urls', namespace='social')),
    # path('login/', login, name='login'),
    # path('logout/', logout_view, name='logout'),
]