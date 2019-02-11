# Generated by Django 2.1.5 on 2019-01-10 22:47

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0015_auto_20190107_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammate',
            name='level',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teammate',
            name='lft',
            field=models.PositiveIntegerField(db_index=True, default=1, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teammate',
            name='manager',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='direct_reports', to='people.Teammate'),
        ),
        migrations.AddField(
            model_name='teammate',
            name='rght',
            field=models.PositiveIntegerField(db_index=True, default=2, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teammate',
            name='tree_id',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teammate',
            name='workday_id',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='teammate',
            name='slack_uid',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]