# Generated by Django 4.2.7 on 2024-01-04 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0017_remove_userinfo_sex_student_sex'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='other_languages_and_levels',
        ),
    ]
