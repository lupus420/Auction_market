import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
'''
Here are the models that are used to create a SQL data objects
with specific parameters
'''

'''
Have to make a funciton to get default category, because otherwise error occur
I cannot access the table 'auctions_auctioncategory' before migration
'''
def get_default_category():
    default_category, _ = AuctionCategory.objects.get_or_create(title='Others')
    return default_category

# AbstractUser already has: username, email, password
class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class AuctionCategory(models.Model):
    title = models.CharField(max_length=64)
    class Meta:
        verbose_name_plural = "Auction categories"
    def __str__(self) -> str:
        return f"{self.title}"
    
class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    category = models.ForeignKey(AuctionCategory, on_delete=models.SET_DEFAULT, default=get_default_category)
    image = models.ImageField(null=True, upload_to="auction_images/%Y/%m")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auction_author")
    watch_list = models.ManyToManyField(User, related_name="watching_listing")
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)
    
    def __str__(self) -> str:
        return f"{self.title}"

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        # Call the superclass's delete() method to perform regular deletion
        super(AuctionListing, self).delete(*args, **kwargs)
    
class AuctionBid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_author")
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False, default=timezone.now)

class AuctionComment(models.Model):
    # ForeignKey: AuctionComment assigned to one AuctionBid - many to one relation
    # on_delete=models.CASCADE : when the referenced object(AuctionBid) is deleted, delete this object
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="commented_auction")
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")