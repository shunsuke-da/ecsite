from django.db import models
from django.db.models import Sum, F
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class BaseInfo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    #Meta内で設定
    class Meta:
        abstract = True # テーブルを作らない抽象クラス

class Items(BaseInfo):
    name = models.CharField(max_length=30, unique=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='items/',blank=True)

    def __str__(self):
        return self.name

class Carts(BaseInfo):
    cart_id = models.BigAutoField(primary_key=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)

    def sum_cart_item_display(self):
        return self.cartitems_set.aggregate(
            total=Sum("quantity")
        )["total"] or 0
    
    def get_total_quantity(self):
        return self.cartitems_set.aggregate(
            total=Sum("quantity")
        )["total"] or 0

    def get_total_price(self):
        return self.cartitems_set.aggregate(
            # モデルのフィールドをそのままDBに計算
            total=Sum(F("quantity") * F("item__price"))
        )["total"] or 0

class CartItems(BaseInfo):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    cart = models.ForeignKey(Carts, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(

                 # カートIDとアイテムでユニーク制約
                fields=["cart", "item"],
                name="cart_item_unique"
            ),
        ]

    def subtotal(self):
        return self.item.price * self.quantity
    



