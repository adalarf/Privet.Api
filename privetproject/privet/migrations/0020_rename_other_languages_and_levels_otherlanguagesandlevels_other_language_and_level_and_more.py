# Generated by Django 4.2.7 on 2024-01-05 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0019_otherlanguagesandlevels_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='otherlanguagesandlevels',
            old_name='other_languages_and_levels',
            new_name='other_language_and_level',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='other_languages_and_levels',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='other_languages_and_levels',
            field=models.ManyToManyField(blank=True, related_name='other_languages_and_levels', to='privet.otherlanguagesandlevels'),
        ),
    ]
