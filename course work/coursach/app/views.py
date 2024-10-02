from rest_framework import viewsets
from .models import Employees, Projects, User, EmployeeProject
from .serializers import EmployeesSerializers, ProjectsSerializers, UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from django.db.models import Q
from .pagination import EmployeesPagination, ProjectsPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

# from django.shortcuts import redirect
# from django.contrib.auth import logout

class EmployeesViewSet(viewsets.ModelViewSet):
    queryset = Employees.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'age', 'salary']                 #/employees/?search=John
    serializer_class = EmployeesSerializers
    pagination_class = EmployeesPagination
    
    enable_filter = False  # Флаг для включения/выключения фильтрации

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.enable_filter:
            queryset = queryset.filter(
                (Q(position='Programmer') | Q(age__gt=50)) & ~Q(salary__lt=4500) #curl -X GET http://localhost:8000/employees/
            )
        return queryset


     #http://127.0.0.1:8000/employees/Age/12/

    @action(methods=['GET'], detail=False, url_path='Age/(?P<age>\d+)')
    def filterEmployeesByAge(self, request, age=None):
        if age is None:
            return Response("Пожалуйста, укажите параметр age в запросе.", status=400)
        try:
            age = int(age)
        except ValueError:
            return Response("Параметр age должен быть числом.", status=400)

        employees = Employees.objects.filter(age=age)
        if not employees:
            raise Http404("Сотрудников с указанным возрастом не найдено.")

        serializer = EmployeesSerializers(employees, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def createEmployee(self, request):
        serializer = EmployeesSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProjectFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializers
    pagination_class = ProjectsPagination
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]   #http://127.0.0.1:8000/projects/?title=Valid
    filterset_class = ProjectFilter
    search_fields = ['title']
    ordering_fields = ['title', 'description']

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# def login(request):
#     return redirect('/auth/login/vk/') 

# def logout_view(request):
#     logout(request)
#     return redirect('/')