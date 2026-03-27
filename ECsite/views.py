from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Items


class ItemIndex(ListView):
    template_name = "item_index.html"
    model = Items
    context_object_name = 'item_list'

class ItemDetail(DetailView):
    template_name = "detail.html"
    model = Items
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        items = Items.objects.order_by("created_at")

        if self.request.user.is_authenticated and context[self.context_object_name]:
        post = context[self.context_object_name]
        post.edit_url = reverse(f'admin:{post._meta.app_label}_{post._meta.model_name}_change', args=[post.id] )
        return context
        

