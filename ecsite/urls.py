from django.urls import path
from .views import ItemListView, ItemDetailView, ManageItemListView, CreateItemView , UpdateItemView, CartDetailView, delete_item, add_one_cart_func, add_some_cart_func,delete_cart_item
from django.views.generic.base import TemplateView
from basicauth.decorators import basic_auth_required
from django.conf import settings

urlpatterns = [
    
     path("index/", ItemListView.as_view(), name="index"),
     path("detail/<int:pk>/", ItemDetailView.as_view(), name="detail"),

     # checkとcart画面
     # cart機能
     path("cart_check/", CartDetailView.as_view(), name="cart_detail"),
     path("cart_check/<int:pk>/delete/", delete_cart_item, name="delete_cart_item"),

     # 商品管理画面
     path("manage/items/", basic_auth_required(ManageItemListView.as_view()), name="manage_items_list"),
     path("manage/items/create/", basic_auth_required(CreateItemView.as_view()), name="create_item"),
     path("manage/items/<int:pk>/update/", basic_auth_required(UpdateItemView.as_view()), name="update_item"),
     path("manage/items/<int:pk>/delete/", basic_auth_required(delete_item), name="delete_item"),

     # カート機能
     path("items/<int:pk>/add_one_cart/", add_one_cart_func, name="add_one_cart"),
     path("items/<int:pk>/add_some_cart/", add_some_cart_func, name="add_some_cart"),
]

