# Generated by Django 2.1.5 on 2019-01-15 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0018_teammate_team_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammate',
            name='okrs',
            field=models.TextField(blank=True),
        ),
    ]
