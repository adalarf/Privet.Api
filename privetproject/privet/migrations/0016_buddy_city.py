# Generated by Django 4.2.7 on 2024-01-04 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0015_buddy_buddy_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='buddy',
            name='city',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
