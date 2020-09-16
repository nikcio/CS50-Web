# Generated by Django 3.1.1 on 2020-09-16 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Home', 'Home'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Other', 'Other')], default='Other', max_length=64),
        ),
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_current', to='auctions.bid'),
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_start', to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.URLField(max_length=1084),
        ),
        migrations.CreateModel(
            name='WatchList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listings', models.ManyToManyField(related_name='watchlist', to='auctions.Listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
