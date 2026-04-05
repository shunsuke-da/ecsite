from django.urls import path
from .views import ItemListView, ItemDetailView, ManageItemListView, CreateItemView , UpdateItemView, delete_item
from basicauth.decorators import basic_auth_required
from django.conf import settings

urlpatterns = [
     path("index/", ItemListView.as_view(), name="index"),
     path("detail/<int:pk>/", ItemDetailView.as_view(), name="detail"),

     # 商品管理画面
     path("manage/items/", basic_auth_required(ManageItemListView.as_view()), name="manage_items_list"),
     path("manage/items/create/", basic_auth_required(CreateItemView.as_view()), name="create_item"),
     path("manage/items/<int:pk>/update/", basic_auth_required(UpdateItemView.as_view()), name="update_item"),
     path("manage/items/<int:pk>/delete/", basic_auth_required(delete_item), name="delete_item"),
]

