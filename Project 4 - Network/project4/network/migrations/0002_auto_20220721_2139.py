# Generated by Django 3.2.5 on 2022-07-21 13:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='users_follower',
            field=models.ManyToManyField(blank=True, related_name='_network_user_users_follower_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='users_following',
            field=models.ManyToManyField(blank=True, related_name='_network_user_users_following_+', to=settings.AUTH_USER_MODEL),
        ),
    ]
