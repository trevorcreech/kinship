# Generated by Django 2.1.5 on 2019-01-13 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0017_auto_20190110_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammate',
            name='team_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]