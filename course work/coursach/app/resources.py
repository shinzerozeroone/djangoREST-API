from import_export import resources
from .models import Employees

class EmployeesResource(resources.ModelResource):
    class Meta:
        model = Employees
        fields = ('name', 'age', 'salary','position')