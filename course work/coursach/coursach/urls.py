from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from app.views import  EmployeesViewSet, ProjectsViewSet, UserViewSet
from django.db.models import Q

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff', 'id', 'first_name', 'last_name']

# ViewSets define the view behavior.
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
]