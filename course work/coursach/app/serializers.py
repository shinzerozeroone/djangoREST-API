from rest_framework import serializers, pagination
from .models import Employees, Projects, User
from .pagination import EmployeesPagination, ProjectsPagination

class EmployeesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Employees
        fields = ['name', 'age', 'salary', 'position']
        pagination_class = EmployeesPagination 

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Сотрудник должен быть старше 18 лет.")
        
        return value

class ProjectsSerializers(serializers.ModelSerializer):
    class Meta: 
        model = Projects
        fields = '__all__'
        pagination_class = ProjectsPagination

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name'] 


