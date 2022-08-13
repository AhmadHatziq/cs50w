# Generated by Django 3.2.5 on 2022-08-01 14:43

from django.db import migrations
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        ('geocache', '0004_auto_20220801_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='geocache',
            name='position',
            field=geoposition.fields.GeopositionField(default=None, max_length=42),
            preserve_default=False,
        ),
    ]