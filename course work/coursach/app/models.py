from django.db import models
from simple_history.models import HistoricalRecords

class Employees(models.Model):
    name = models.TextField(max_length = 20)
    age = models.IntegerField()
    salary = models.IntegerField()
    position = models.TextField(max_length = 50)
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
class Projects(models.Model):
    title = models.CharField(max_length = 30)
    description = models.TextField(max_length = 100)
    history = HistoricalRecords()
    def __str__(self):
        return self.title
    
class EmployeeProject(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE, verbose_name = 'Сотрудник', help_text="Назначьте сотрудника")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, verbose_name = 'Проект', help_text="Назначьте проект")
    date_created = models.DateField(null = True, blank = True)
    history = HistoricalRecords()
    def __str__(self):
        return str(self.pk)

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    history = HistoricalRecords()
    def __str__(self):
        return f'{self.first_name} {self.last_name}'