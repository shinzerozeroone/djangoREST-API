from django.contrib import admin
from .models import Employees, Projects, EmployeeProject, User
from import_export.admin import ExportActionMixin
from django.http import HttpResponse, HttpResponseBadRequest
from .resources import EmployeesResource
import csv


class EmployeeProjectInline(admin.TabularInline):
    model = EmployeeProject


@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin, ExportActionMixin):
    list_display = ('name', 'age', 'salary', 'position')
    list_filter = ['age']
    list_display_links = ('name', 'age')
    actions = ['export_admin_action']
    
    def export_admin_action(self, request, queryset):
        formats = {
            'csv': 'CSV',
            'xlsx': 'Excel',
        }

        if request.GET.get('export_format'):
            export_format = request.GET['export_format']
        else:
            export_format = list(formats.keys())[1]

        response = HttpResponse(content_type=formats.get(export_format))
        response['Content-Disposition'] = f'attachment; filename=export.{export_format}'

        if export_format == 'xlsx':
            xlsx_data = csv.writer(response)
            xlsx_data.writerow(EmployeesResource().get_export_headers())
            for row in queryset:
                xlsx_data.writerow(EmployeesResource().export_resource(row))
        elif export_format == 'cvs':
            csv_data = EmployeesResource()
            dataset = csv_data.export(queryset)
            dataset.export(response)
        else:
            return HttpResponseBadRequest("Unsupported format selected")

        return response

    export_admin_action.short_description = "Export selected objects"

@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin,):
    list_display = ('title', 'description')
    list_filter = ['title']
    inlines = [EmployeeProjectInline]

@admin.register(EmployeeProject)
class EmployeeProjectAdmin(admin.ModelAdmin):
    list_display = ('employee', 'project', 'date_created')
    list_filter = ['employee', 'project','date_created']
    date_hierarchy = 'date_created'
    raw_id_fields =["employee"]
    readonly_fields = ["date_created"]
    search_fields = ["employee", "project"]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass