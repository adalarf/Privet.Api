# Generated by Django 4.2.7 on 2024-01-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0029_remove_student_confirmation_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
