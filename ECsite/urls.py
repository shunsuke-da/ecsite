
from django.urls import path
from django.views.generic.base import TemplateView

urlpatterns = [
    path('hello/', TemplateView.as_view(template_name='hello.html')),
]
