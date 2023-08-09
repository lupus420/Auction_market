from django.contrib import admin
from .models import AuctionBid, AuctionComment, AuctionListing, User, AuctionCategory
'''
admin
admin123
'''

# Register your models here.
admin.site.register(AuctionBid)
admin.site.register(AuctionComment)
admin.site.register(AuctionListing)
admin.site.register(User)
admin.site.register(AuctionCategory)