# Generated by Django 2.1.5 on 2019-01-05 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0008_auto_20190105_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammate',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='teammate',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]