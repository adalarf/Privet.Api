# Generated by Django 4.2.7 on 2023-12-20 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0008_alter_buddyarrival_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='arrivalbooking',
            name='arrival_point',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='arrivalbooking',
            name='comment',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='arrivalbooking',
            name='flight_number',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]