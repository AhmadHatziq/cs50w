# Generated by Django 3.2.5 on 2022-06-06 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20220606_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='item_bid_amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=9),
        ),
    ]