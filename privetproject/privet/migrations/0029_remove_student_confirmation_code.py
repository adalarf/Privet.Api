# Generated by Django 4.2.7 on 2024-01-13 08:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0028_alter_student_confirmation_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='confirmation_code',
        ),
    ]