# Generated by Django 4.2.7 on 2024-01-13 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0030_student_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='full_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
