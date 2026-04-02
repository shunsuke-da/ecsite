from django.urls import path
from .views import ItemIndex, ItemDetail
from django.views.generic.base import TemplateView


urlpatterns = [
     path("index/", ItemIndex.as_view(), name="index"),
     path("detail/<int:pk>", ItemDetail.as_view(), name="detail"),
]

