# Generated by Django 4.1.5 on 2023-04-17 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_employees_stress'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='message',
            field=models.BooleanField(default='False'),
        ),
    ]