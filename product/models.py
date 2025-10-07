from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(("Name"), max_length=100)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    image2 = models.ImageField(upload_to="products/", null=True, blank=True)
    image3 = models.ImageField(upload_to="products/", null=True, blank=True)
    image4 = models.ImageField(upload_to="products/", null=True, blank=True)
    brand = models.CharField(("Brand"), max_length=100)
    price = models.FloatField(("Price"))
    discount = models.IntegerField(("Discount"), null=True, blank=True)
    detail = models.TextField(("Detail"))
    is_closed = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
    
class Review(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.rating}★"
    
class Biding(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bid_amount = models.IntegerField("Bid Amount", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.bid_amount}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["item", "user"], name="unique_bid_per_user_per_item")
        ]



