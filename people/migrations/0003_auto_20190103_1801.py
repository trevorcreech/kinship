# Generated by Django 2.1.4 on 2019-01-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20190103_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammate',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='teammate',
            name='start_date',
            field=models.DateField(null=True),
        ),
    ]
