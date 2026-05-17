from .models import Carts

def get_cart(self):
    if not self.request.session.session_key:
            self.request.session.create()
    return Carts.objects.get_or_create(
        session_key=self.request.session.session_key
    )

def get_cart_from_request(request):
    if not request.session.session_key:
        request.session.create()
    return Carts.objects.get_or_create(
        session_key= request.session.session_key
    )