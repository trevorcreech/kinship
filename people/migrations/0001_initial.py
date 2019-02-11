# Generated by Django 2.1.4 on 2019-01-03 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PropsMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Teammate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_uid', models.CharField(max_length=255, unique=True)),
                ('slack_display_name', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('phone', models.CharField(blank=True, max_length=255)),
                ('image', models.URLField(blank=True)),
                ('start_date', models.DateField(blank=True)),
                ('birthday', models.DateField(blank=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='propsmessage',
            name='user_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='giver', to='people.Teammate'),
        ),
        migrations.AddField(
            model_name='propsmessage',
            name='user_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver', to='people.Teammate'),
        ),
    ]