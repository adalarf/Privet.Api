# Generated by Django 4.2.7 on 2024-01-04 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('privet', '0018_remove_userinfo_other_languages_and_levels'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherLanguagesAndLevels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_languages_and_levels', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='other_languages_and_levels',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='privet.otherlanguagesandlevels'),
        ),
    ]
