# Generated by Django 3.2.5 on 2022-06-06 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctions_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='category',
        ),
        migrations.AlterField(
            model_name='auctions',
            name='item_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.category'),
        ),
    ]
