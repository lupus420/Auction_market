# Generated by Django 4.2.3 on 2023-08-08 08:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0008_auctionlisting_watch_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="auctionbid",
            name="date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="auctionlisting",
            name="date_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="auctionbid",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
