# Generated by Django 3.1.1 on 2020-09-16 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200916_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Electronics', 'Electronics'), ('Home', 'Home'), ('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Other', 'Other')], default='Other', max_length=64),
        ),
        migrations.AlterField(
            model_name='listing',
            name='current_bid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='listing_current', to='auctions.bid'),
        ),
    ]
