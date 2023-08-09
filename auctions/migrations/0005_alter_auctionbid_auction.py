# Generated by Django 4.2.3 on 2023-08-05 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_rename_desctiprion_auctionlisting_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="auctionbid",
            name="auction",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bid",
                to="auctions.auctionlisting",
            ),
        ),
    ]
