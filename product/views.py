from django.shortcuts import render , HttpResponse, redirect, get_object_or_404
from product.models import Item, Review, Biding
from django.db.models import Max
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def item(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        brand = request.POST['brand']
        detail = request.POST['detail']
        price = request.POST['price']
        discount = request.POST['discount']
        
        item = Item(name=name, image=image,image2=image2,image3=image3,image4=image4, price=price,discount=discount, brand=brand, detail=detail)
        item.save()

def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    reviews = Review.objects.filter(item=item)
    highest_bid = item.bids.aggregate(Max("bid_amount"))["bid_amount__max"]
    bidings = item.bids.all().order_by('-created_at')


    user_has_bid = False
    if request.user.is_authenticated:
        user_has_bid = Biding.objects.filter(item=item, user=request.user).exists()
    
    context = {
        'item': item,
        'bidings': bidings,
        'reviews': reviews,
        'highest_bid': highest_bid,
        'user_has_bid': user_has_bid,
    }

    return render(request, 'item_detail.html', context)

@login_required
def add_review(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        name = request.POST["name"]
        rating = request.POST["rating"]
        comment = request.POST["comment"]

        Review.objects.create(
            user=request.user,
            item=item,
            name=name,
            rating=rating,
            comment=comment
        )
        return redirect("item_detail", id=item.id)  # back to detail page

    return render(request, "add_review.html", {"item": item})

def item_upload_form(request):
    if request.method == "POST":
        name = request.POST['name']
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        price = request.POST['price']
        discount = request.POST['discount']
        brand = request.POST['brand']
        description = request.POST['description']

        item = Item(   # ✅ use model class here
            user=request.user,
            name=name,
            image=image,
            image2=image2,
            image3=image3,
            image4=image4,
            price=price,
            discount=discount,
            brand=brand,
            detail=description
        )
        item.save()

        return redirect('index')
    return render(request, 'form.html')

@login_required
def my_list(request):
    items = Item.objects.filter(user=request.user)
    return render(request, "my_list.html", {"items": items})

@login_required
def item_edit(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        name = request.POST['name']
        image = request.FILES.get('image')
        image2 = request.FILES.get('image2')
        image3 = request.FILES.get('image3')
        image4 = request.FILES.get('image4')
        brand = request.POST['brand']
        detail = request.POST['detail']
        price = request.POST['price']
        discount = request.POST['discount']

        if not name or not brand or not detail or not discount or not price:
            return render(request, 'item_edit.html', {
                'item': item,
                'error': 'Please fill in all fields.'
            })

        item.name = name
        item.brand = brand
        item.detail = detail
        item.discount = discount
        item.price = price

        if image:
            item.image = image
            item.image2 = image2
            item.image3 = image3
            item.image4 = image4

        item.save()
        return redirect('my_list')   # go back to "my list" page

    # this handles GET requests (show the form)
    return render(request, 'item_edit.html', {'item': item})

@login_required
def item_delete(request, id):
    item = get_object_or_404(Item, id=id)
    item.delete()
    return redirect('my_list')   # go back to "my list" page 

@login_required
def add_bids(request, id):
    item = get_object_or_404(Item, id=id)

    if request.method == "POST":
        bid_amount = request.POST["bid_amount"]

        Biding.objects.create(
            user=request.user,
            item=item,
            bid_amount=bid_amount,
        )
        return redirect("item_detail", id=item.id)  # back to detail page
    
    return render(request, "add_bids.html", {"item": item})

@login_required
def bid_edit(request, id):
    item = get_object_or_404(Item, id=id)
    bid, created = Biding.objects.get_or_create(item=item, user=request.user)

    if request.method == "POST":
        bid_amount = request.POST.get("bid_amount")

        if not bid_amount:
            return render(request, "bid_edit.html", {
                "item": item,
                "bid": bid,
                "error": "Please enter a bid amount."
            })

        bid.bid_amount = bid_amount
        bid.created_at = timezone.now()  # update timestamp
        bid.save()
        return redirect("item_detail", id=item.id)

    return render(request, "bid_edit.html", {"item": item, "bid": bid})

@login_required
def bid_delete(request, id):
    item = get_object_or_404(Item, id=id)
    bid = get_object_or_404(Biding, item=item, user=request.user)
    bid.delete()
    return redirect('item_detail', id=item.id)   # go back to "item detail" page

@login_required
def close_bid(request, id):
    item = get_object_or_404(Item, id=id)
    if request.user == item.user:  # only the owner
        item.is_closed = True
        item.save()
    return redirect('item_detail', id=id)  # or your detail view name

@login_required
def reopen_bid(request, id):
    item = get_object_or_404(Item, id=id)
    if request.user == item.user:  # only owner can reopen
        item.is_closed = False
        item.save()
    return redirect('item_detail', id=id)
