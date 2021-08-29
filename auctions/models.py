from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.forms import ModelForm


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listings', blank=True)
    
class Category(models.Model):
    
    title = models.CharField(max_length=32 )

    def __str__(self):
        return f"{self.title}"

class Listings(models.Model):
    #pass
    creator = models.ForeignKey(User, on_delete=models.CASCADE , related_name="creator")
    item = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=8 , decimal_places=2 , default=0 )
    image = models.URLField(null=True , blank=True)
    description = models.TextField(max_length=900)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name="category")
    status = models.BooleanField(default=True)
    timestart = models.DateTimeField(default=datetime.now())
    timeend = models.DateTimeField(null=True , blank=True)

    def __str__(self):
        return f" {self.item} : ${self.price} by {self.creator}"


class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids")
    bidprice = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f"${self.bidprice} by {self.user} at {self.timestamp}"


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.user} - {self.content}"

