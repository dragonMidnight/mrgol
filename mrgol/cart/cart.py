from django.contrib.sessions.backends.db import SessionStore

from .models import SesKey
from app1.models import Product
from app1.myserializers import ProductDetailSerializer




#mrgol/cart changes vs myshop/cart:     1- change ob to seskey_obj   2- use user cookie instead session for unauthentication users(more optimize)  3- remove def add(this will done in fron)  4- remove self.session and def save(dont connect to database for every request of authenticated user), instead we use just data sended from user(self.ids), save shoude be done in lgout and loadin self.ids should be done in login     5-  optimize __iter__ query    6- do serializing in cart(it is better)
class Cart:

    def __init__(self, request):
        self.ids = request.COOKIES.get('favorite_products_ids').split(',') if request.COOKIES.get('favorite_products_ids') else []         #request.COOKIES.get('favorite_products_ids') should be like: "1,2,3,4",   in front should be done like: COOKIES['favorite_products_ids'] = ids_in_cookie + current_id(if provided),   cares about removing dublicates' ids should be done in front.  curent_id is like when you click on button "ezae kardan be alaqemandi ha" on specific product, that id isnt in cookie. it must sum with ids in cookie and set that id to cookie in response. 
            
    def remove(self, product_id):
        if product_id in self.ids:
            self.ids.remove(product_id)

    def get_products(self):
        products = Product.objects.filter(id__in=self.ids)
        return ProductDetailSerializer(products, many=True).data

    def get_products_numbers(self):
        return len(self.ids)
            





