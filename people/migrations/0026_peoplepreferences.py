# Generated by Django 2.1.5 on 2019-02-03 02:53

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('preferences', '0002_auto_20181220_0803'),
        ('people', '0025_auto_20190129_2143'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeoplePreferences',
            fields=[
                ('preferences_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='preferences.Preferences')),
                ('enable_google', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'People Directory Preferences',
            },
            bases=('preferences.preferences',),
            managers=[
                ('singleton', django.db.models.manager.Manager()),
            ],
        ),
    ]