# Generated by Django 3.1.1 on 2020-11-01 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes',
            field=models.ManyToManyField(related_name='likers', to='network.Post'),
        ),
    ]
