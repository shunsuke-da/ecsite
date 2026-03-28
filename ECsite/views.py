from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .models import Items


class ItemIndex(ListView):
    template_name = "index.html"
    model = Items
    context_object_name = 'item_list'

class ItemDetail(DetailView):
    template_name = "detail.html"
    model = Items
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 今表示している商品
        current_item = self.object

        # 今の商品以外で、商品一覧から作成された新しい順で４つを出す。
        context['new_item_list'] = Items.objects.exclude(id=current_item.id).order_by('-created_at')[:4]
        return context
        

