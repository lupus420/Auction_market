# Generated by Django 4.2.3 on 2023-08-05 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0006_alter_auctionlisting_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionbid",
            name="auction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bids",
                to="auctions.auctionlisting",
            ),
        ),
    ]
