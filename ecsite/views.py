from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, redirect,render
from django.urls import reverse_lazy
from .models import Items, Carts, CartItems


class ItemListView(ListView):
    template_name = "index.html"
    model = Items
    context_object_name = 'item_list'

class ItemDetailView(DetailView):
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


# 管理画面
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

# カート機能
def add_one_cart_func(request, pk):
    # セッションに関すること必要？
    # POST
    # 分岐：まず、ユーザのカートがあるか、
    # あれば　⇨ ITEM_CARTにあるか確認
        # あれば ⇨　個数追加
        # なければ(新しいアイテムであれば) ⇨　ITEM_CART追加 

    # なければ. ⇨ INSERT （カートテーブル、アイテムカートテーブル）
    # 最後に個数を表示ように返す
    if request.method == "POST":
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key

        cart, created = Carts.objects.get_or_create(session_key=session_key)

        cart_item = CartItems.objects.filter(
            cart=cart,
            item_id=pk
        ).first()
            # cart_object = get_object_or_404(Carts,cart_id=cart_id)

            # カートがあれば（一度でもアイテムをカートに入れていれば）
            # cart_item = get_object_or_404(CartItems,item_id=pk)

            # カートアイテムがあれば（カートへ同じ商品を追加であれば）
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItems(cart=cart, item_id=pk, quantity=1)

        cart_item.save()
        return redirect('index')

def add_some_cart_func(request, pk):
    return
    # some・個数を受け取る
    # ロジックは上と同じ

