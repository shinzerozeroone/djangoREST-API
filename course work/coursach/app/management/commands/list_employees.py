from django.core.management.base import BaseCommand
from app.models import Employees

class Command(BaseCommand):
    help = 'Lists all employees'   

    def handle(self, *args, **options):
        employees = Employees.objects.all()

        if employees.exists():
            for employee in employees:
                self.stdout.write(f'Name: {employee.name}, Age: {employee.age}, Salary: {employee.salary}, Position: {employee.position}')
        else:
            self.stdout.write('No employees found.')


#python manage.py list_employees