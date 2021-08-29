from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User,Listings,Category,Bids,Comments


def index(request):

    listings = Listings.objects.filter(status=True).order_by('-timestart')
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newlisting(request):
    categories = Category.objects.order_by('title').values_list('title', flat=True)
    if request.user.is_authenticated:
        username = request.user
    else:
        return render(request,"auction/login.html", {
            "message": "Please login first. "
        }) 
    if request.method == "POST":
        if request.POST.get('image') is None:
            image = "https://i.imgur.com/OaN3lMh.jpg"
        else:
            image = request.POST.get('image')
        
        lst = Listings(
            creator = username,
            item = request.POST.get('item').capitalize(),
            price = request.POST.get('price'),
            image = image,
            description = request.POST.get('description'),
            timestart= datetime.now(),
            category = Category.objects.get(title=request.POST.get('category'))
        )

        lst.save()
        #return HttpResponseRedirect(reverse("index"))
        return render(request , "auctions/newlisting.html",{
            "categories" : categories,
            "message": "Listing successfully Added! "
        })
    
    return render(request, "auctions/newlisting.html",{
        "categories": categories}
    )

def listingpage(request , listing_id):
    categories = Category.objects.order_by('title').values_list('title', flat=True)
    listing = Listings.objects.get(pk=listing_id)
    if not request.user.is_authenticated:
        return render(request, "auctions/listing.html",{
            "listing":Listings.objects.get(id=listing_id),
            "message":2,
            "category":categories
        })
    #code for wishlist
    in_watchlist = False
    if Listings.objects.get(id=listing_id) in User.objects.get(id=request.user.id).watchlist.all():
        in_watchlist=True
    creator = False
    
    if Listings.objects.get(id=listing_id).creator == request.user:
        creator = True
    if request.method == "POST":
        if request.POST["type"] == "Comment":
            comment(request,listing)
            return HttpResponseRedirect(reverse("listingpage",args=[listing_id]))

        elif request.POST["type"] == "Bid" :
            oldprice=listing.price
            if listing.bids.exists():
                oldprice = Listings.objects.get(pk=listing_id).bids.last().bidprice 

            if float(oldprice)==float(request.POST.get('bid')) or float(oldprice)>float(request.POST.get('bid')) :
                return render(request, "auctions/listing.html",{
                    #somecode\
                    "listing":Listings.objects.get(id=listing_id),
                    "message": 0, #low value bid unsuccess
                    "creator": creator,
                    "in_watchlist":in_watchlist,
                    "category":categories
                })
            bid = Bids(
                user = request.user,
                listing = Listings.objects.get(id=listing_id),
                bidprice = float(request.POST.get('bid')),
                timestamp = datetime.now()
            )
            bid.save()
            return render(request,"auctions/listing.html", {
                    #somecode
                "listing":Listings.objects.get(id=listing_id),
                "message": 1, #bid placed success
                "creator": creator,
                "in_watchlist":in_watchlist,
                "category":categories
            })

    return render(request,"auctions/listing.html",{
        "listing":Listings.objects.get(id=listing_id),
        "creator": creator,
        "in_watchlist":in_watchlist,
        "category":categories
    })
       
   
def mylisting(request):
    if request.method == "POST":
        lst = Listings.objects.get(id=request.POST.get('closebid'))
        lst.timeend = datetime.now()
        lst.status = False
        lst.save()
        return HttpResponseRedirect(reverse("listingpage", kwargs = {"listing_id":request.POST.get('closebid')}))

       # return render (request, "auctions/listing.html",{"listing":Listings.objects.get(id=request.POST.get('closebid'))})
    listings = Listings.objects.filter(creator=request.user).order_by('-timestart')
    return render(request, "auctions/mylisting.html",{
        "listings":listings
    })

def comment(request,listing):

    if not request.POST["content"]:
        return render(request, "auctions/listing.html",{
            "listings":listing,
            "message" :3 #message as : Plese enter comment
        })
        
    comment = Comments(
        user = User.objects.get(pk=request.user.id),
        listing = listing,
        content = request.POST["content"]
    )

    comment.save()

def categories(request):
    return render(request,"auctions/categories.html",{
        "categories": Category.objects.all()
    })

def category_page(request, listing_id):
    return render(request,"auctions/category_page.html",{
        "listings": Listings.objects.filter(category = Category.objects.get(id=listing_id)).filter(status=True).all(),
        "category": Category.objects.get(id=listing_id)
    })

def watchlist(request):
    return render(request,"auctions/watchlist.html",{
        "listings":request.user.watchlist.all()
    })

def watchlist_move(request,listing_id):
    if Listings.objects.get(id=listing_id) in request.user.watchlist.all():
        request.user.watchlist.remove(Listings.objects.get(id=listing_id))
    else:
        request.user.watchlist.add(Listings.objects.get(id=listing_id))

    return HttpResponseRedirect(reverse("listingpage", args=(listing_id,)))


























