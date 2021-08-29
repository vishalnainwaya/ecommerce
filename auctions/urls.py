from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("<int:listing_id>", views.listingpage , name="listingpage"),
    path("mylisting",views.mylisting, name="mylisting"),
    path("categories", views.categories, name="categories"),
    path("category_page/<int:listing_id>",views.category_page,name="category_page"),
    path("watchlist/<int:listing_id>", views.watchlist_move, name="watchlist_move"),
    path("watchlist", views.watchlist,name="watchlist")
]
