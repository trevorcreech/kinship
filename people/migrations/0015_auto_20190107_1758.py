# Generated by Django 2.1.5 on 2019-01-08 01:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0014_auto_20190107_1138'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='propsmessage',
            options={'ordering': ('-sent_on',)},
        ),
    ]
