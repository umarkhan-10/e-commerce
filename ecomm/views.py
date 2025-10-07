from django.http import HttpResponse
from django.shortcuts import render,redirect
from product.models import Item
 
def index(request):
    items = Item.objects.all()   # get all records
    context = {
        "items": items           # pass the queryset, not the class
    }
    return render(request, 'index.html', context)

