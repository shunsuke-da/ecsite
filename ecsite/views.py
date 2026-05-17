from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView,TemplateView
from django.shortcuts import get_object_or_404, redirect,render
from django.db.models import F, Sum
from django.urls import reverse_lazy
from .models import Items, Carts, CartItems
from django.views.decorators.http import require_POST

from .utils import get_cart, get_cart_from_request

class ItemListView(ListView):
    template_name = "index.html"
    model = Items
    context_object_name = 'item_list'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)

            # セッションの確認＋カート取得
            cart, _ = get_cart(self)

            context["cart_quantity"] = cart.sum_cart_item_display()
            return context

class ItemDetailView(DetailView):
    template_name = "detail.html"
    model = Items
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 今表示している商品
        current_item = self.object

        # セッションの確認＋カート取得
        cart, _ = get_cart(self)

        # 今の商品以外で、商品一覧から作成された新しい順で４つを出す。
        context['new_item_list'] = Items.objects.exclude(id=current_item.id).order_by('-created_at')[:4]
        context["cart_quantity"] = cart.sum_cart_item_display()
        return context 

########## 管理画面 #########
class ManageItemListView(ListView):
    template_name = "manage/items.html"
    model = Items
    context_object_name = 'items'

class CreateItemView(CreateView):
    template_name = "manage/create_update_item.html"
    model = Items
    fields = ('name', 'price', 'description' , 'image')
    success_url = reverse_lazy('manage_items_list')

class UpdateItemView(UpdateView):
    template_name = "manage/create_update_item.html"
    model = Items
    fields = ('name', 'price', 'description' , 'image')
    success_url = reverse_lazy('manage_items_list')

def delete_item(request, pk):
    item = get_object_or_404(Items, pk=pk)
    
    if request.method == "POST":
        item.delete()
    
    return redirect('manage_items_list')
############################

########## カート& チェックアウト画面 #########

########## カート機能 #########

class CartDetailView(TemplateView):
    template_name = "cart_check.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # セッションの確認＋カート取得
        cart, _ = get_cart(self)

        # カートアイテム取得（全部取る）
        cart_items = CartItems.objects.filter(cart=cart).select_related("item")

        context["cart_items"] = cart_items
        context["total_price"] = cart.get_total_price()
        context["total_quantity"] = cart.sum_cart_item_display()

        return context
    
@require_POST
def delete_cart_item(request, pk):
    # カートとアイテムIDで、そのユーザのカートアイテムを全て削除
    # p: pkはitem_id
    
    # Postで受け取る
    if request.method == "POST":
        
        # セッションの確認＋カート取得
        cart, _ = get_cart_from_request(request)

        # カートアイテム取得
        cart_item = CartItems.objects.filter(
            cart=cart,
            item_id=pk
        )
        cart_item.delete()
    
    return redirect('cart_detail')    

@require_POST
def add_one_cart_func(request, pk, added_quantity=1):

    # Postで受け取る
    if request.method == "POST":
        
        # セッションの確認＋カート取得
        cart, _ = get_cart_from_request(request)

        # カートアイテム取得
        cart_item, created = CartItems.objects.get_or_create( 
            cart=cart, item_id=pk, defaults={'quantity': added_quantity} 
            )
        # なければ、カートアイテム作成
        if not created: 
            CartItems.objects.filter(pk=cart_item.pk).update(quantity=F('quantity') + added_quantity)

        return redirect('index')
    
@require_POST
def add_some_cart_func(request, pk):

        # Postで受け取る
    if request.method == "POST":
        
        added_quantity = int(request.POST['quantity'])

        # セッションの確認＋カート取得
        cart, _ = get_cart_from_request(request)

        # カートアイテム取得
        cart_item = CartItems.objects.filter(
            cart=cart,
            item_id=pk
        ).first()

        # カートアイテムがあれば（カートへ同じ商品を追加であれば）
        if cart_item:
            cart_item.quantity += added_quantity
        # なければ、カートアイテム作成
        else:
            cart_item = CartItems(cart=cart, item_id=pk, quantity=added_quantity)

        # 保存
        cart_item.save()
        return redirect('detail', pk)
############################





