from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing_id"),
    path("<int:listing_id>/bid", views.bid_listing, name="bid_listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name='new_listing'),
    path("error", views.error, name="error"),
    path("delete/<int:listing_id>", views.delete, name="delete_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/add/<int:listing_id>", views.add_to_watchlist, name="add_to_watchlist")
]

if settings.DEBUG:
    urlpatterns=urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)