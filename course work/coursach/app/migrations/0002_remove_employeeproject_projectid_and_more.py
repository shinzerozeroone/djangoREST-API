# Generated by Django 4.2.9 on 2024-02-05 19:20

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employeeproject',
            name='projectID',
        ),
        migrations.AddField(
            model_name='employeeproject',
            name='projectID',
            field=models.CharField(default=100, help_text='Назнач проект', max_length=20, verbose_name=app.models.Projects),
            preserve_default=False,
        ),
    ]