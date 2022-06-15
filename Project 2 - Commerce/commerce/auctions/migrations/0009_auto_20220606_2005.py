# Generated by Django 3.2.5 on 2022-06-06 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auction_item_bid_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='item_bid_amount',
        ),
        migrations.RemoveField(
            model_name='auction',
            name='item_bid_count',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_string', models.CharField(max_length=255)),
                ('comment_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.auction')),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.DecimalField(decimal_places=2, max_digits=9)),
                ('bid_bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('bid_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auctions.auction')),
            ],
        ),
    ]