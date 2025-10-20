from django.shortcuts import render , HttpResponse, redirect, get_object_or_404
from product.models import Item, Review, Biding, Like, Category, Cart
from django.db.models import Max
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def search_items(request):
    query = request.GET.get('q', '')
    items = Item.objects.filter(name__icontains=query) if query else Item.objects.none()
    return render(request, 'search.html', {'items': items, 'query': query})

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

def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    reviews = Review.objects.filter(item=item)
    highest_bid = item.bids.aggregate(Max("bid_amount"))["bid_amount__max"]
    bidings = item.bids.all().order_by('-created_at')


    user_has_bid = False
    if request.user.is_authenticated:
        user_has_bid = Biding.objects.filter(item=item, user=request.user).exists()

    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(user=request.user, item=item).exists()    
    
    context = {
        'item': item,
        'bidings': bidings,
        'reviews': reviews,
        'highest_bid': highest_bid,
        'user_has_bid': user_has_bid,
        'user_liked': user_liked,
    }

    return render(request, 'item_detail.html', context)

@login_required
def add_review(request, slug):
    item = get_object_or_404(Item, slug=slug)

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
        return redirect("item_detail", slug=item.slug)  # back to detail page

    return render(request, "add_review.html", {"item": item})

def item_upload_form(request):
    categories = Category.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id) if category_id else None
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
            category=category,
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
    return render(request, 'form.html' , {'categories': categories})

@login_required
def my_list(request):
    items = Item.objects.filter(user=request.user)
    return render(request, "my_list.html", {"items": items})

@login_required
def my_like(request):
    likes = Like.objects.filter(user=request.user).select_related("item")
    items = [like.item for like in likes]
    return render(request, "my_like.html", {"items": items})

@login_required
def item_edit(request, slug):
    item = get_object_or_404(Item, slug=slug)

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
def item_delete(request, slug):
    item = get_object_or_404(Item, slug=slug)
    item.delete()
    return redirect('my_list')   # go back to "my list" page 

@login_required
def add_bids(request, slug):
    item = get_object_or_404(Item, slug=slug)

    if request.method == "POST":
        bid_amount = request.POST["bid_amount"]

        Biding.objects.create(
            user=request.user,
            item=item,
            bid_amount=bid_amount,
        )
        return redirect("item_detail", slug=item.slug)  # back to detail page
    
    return render(request, "add_bids.html", {"item": item})

@login_required
def bid_edit(request, slug):
    item = get_object_or_404(Item, slug=slug)
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
        return redirect("item_detail", slug=item.slug)

    return render(request, "bid_edit.html", {"item": item, "bid": bid})

@login_required
def bid_delete(request, slug):
    item = get_object_or_404(Item, slug=slug)
    bid = get_object_or_404(Biding, item=item, user=request.user)
    bid.delete()
    return redirect('item_detail', slug=item.slug)   # go back to "item detail" page

@login_required
def close_bid(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.user == item.user:  # only the owner can close
        highest_bid = Biding.objects.filter(item=item).order_by('-bid_amount').first()
        if highest_bid:
            item.winner = highest_bid.user
        item.is_closed = True
        item.save()
    return redirect('item_detail', slug=slug)

@login_required
def reopen_bid(request, slug):
    item = get_object_or_404(Item, slug=slug)
    if request.user == item.user:  # only owner can reopen
        item.is_closed = False
        item.save()
    return redirect('item_detail', slug=slug)

@login_required
def toggle_like(request, slug):
    item = get_object_or_404(Item, slug=slug)
    like, created = Like.objects.get_or_create(user=request.user, item=item)

    if not created:
        # already liked → unlike
        like.delete()

    return redirect('item_detail', slug=slug)

@login_required
def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    items = Item.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'items': items})

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.info(request, "Item quantity updated in your cart.")
    else:
        messages.success(request, "Item added to your cart.")
    
    return redirect('my_cart')  # or change to redirect('item_detail', slug=item.slug)

@login_required
def my_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render(request, 'my_cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    Cart.objects.filter(user=request.user, item=item).delete()
    messages.success(request, "Item removed from your cart.")
    return redirect('cart_view')

def update_cart_quantity(request, slug):
    if request.method == 'POST':
        item = get_object_or_404(Item, slug=slug)
        cart_item = get_object_or_404(Cart, item=item, user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('my_cart')
