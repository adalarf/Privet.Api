# Generated by Django 4.2.7 on 2024-01-03 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0011_user_is_teamlead'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]