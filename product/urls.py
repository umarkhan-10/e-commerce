from django.urls import path
from .views import item, item_detail,item_edit,item_delete, add_review, item_upload_form, my_list, add_bids, bid_edit, bid_delete, close_bid, reopen_bid, toggle_like, my_like, category_view
from .views import add_to_cart, my_cart, remove_from_cart, update_cart_quantity


urlpatterns = [

    path('', item, name='item'),
    path('item/<slug:slug>', item_detail, name='item_detail'),
    path("item/<slug:slug>/edit", item_edit, name="item_edit"),
    path("item/<slug:slug>/bids", add_bids, name="add_bids"),
    path("item/<slug:slug>/bid_edit", bid_edit, name="bids_edit"),
    path("item/<slug:slug>/bid_delete", bid_delete, name="bid_delete"),
    path("item/<slug:slug>/delete", item_delete, name="item_delete"),
    path("item/<slug:slug>/review", add_review, name="add_review"),
    path("item/<slug:slug>/close_bid", close_bid, name="close_bid"),
    path('item/<slug:slug>/reopen/', reopen_bid, name='reopen_bid'),
    path('item/<slug:slug>/like/', toggle_like, name='toggle_like'),
    path('item-upload', item_upload_form, name='item_upload_form'),
    path("category/<slug:slug>/", category_view, name="category"),
    path('cart/update/<slug:slug>/', update_cart_quantity, name='update_cart_quantity'),


    path('cart/add/<slug:slug>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<slug:slug>/', remove_from_cart, name='remove_from_cart'),

    path('cart/', my_cart, name='my_cart'),

    path('my_list', my_list, name='my_list'),
    path("my-like/", my_like, name="my_like"),

]
