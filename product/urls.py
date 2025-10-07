from django.urls import path
from .views import item, item_detail,item_edit,item_delete, add_review, item_upload_form, my_list, add_bids, bid_edit, bid_delete, close_bid, reopen_bid


urlpatterns = [

    path('', item, name='item'),
    path('item/<int:id>', item_detail, name='item_detail'),
    path("item/<int:id>/edit", item_edit, name="item_edit"),
    path("item/<int:id>/bids", add_bids, name="add_bids"),
    path("item/<int:id>/bid_edit", bid_edit, name="bids_edit"),
    path("item/<int:id>/bid_delete", bid_delete, name="bid_delete"),
    path("item/<int:id>/delete", item_delete, name="item_delete"),
    path("item/<int:id>/review", add_review, name="add_review"),
    path("item/<int:id>/close_bid", close_bid, name="close_bid"),
    path('item/<int:id>/reopen/', reopen_bid, name='reopen_bid'),
    path('item-upload', item_upload_form, name='item_upload_form'),
    path('my_list', my_list, name='my_list'),

]
