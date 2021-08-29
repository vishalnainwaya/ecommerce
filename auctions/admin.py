from django.contrib import admin
from .models import Listings,Bids,Category,Comments, User
# Register your models here.

admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(User)