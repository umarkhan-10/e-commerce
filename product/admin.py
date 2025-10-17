from django.contrib import admin
from .models import Item, Review, Biding, Like, Category, Cart

# Register your models here.
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Biding)
admin.site.register(Like)
admin.site.register(Category)
admin.site.register(Cart)