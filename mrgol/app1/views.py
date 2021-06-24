from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache
#from django.template.defaultfilters import slugify
from django.utils.text import slugify
from django.core.mail import send_mail
from django.middleware.csrf import get_token
from django.contrib.sessions.backends.db import SessionStore

from rest_framework import viewsets
from rest_framework import generics, mixins
from rest_framework import permissions, authentication
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import views


from . import myserializers, myforms
from .mymethods import get_products, get_posts, get_posts_products_by_roots, get_childs_and_root
from .models import Comment, Content, Post, Rating, Product ,Root, Filter, Filter_Attribute
from users.myserializers import UserSerializer, UserChangeSerializer
from cart.models import SesKey
from cart.cart import Cart

from django.db.models import Max, Min, PositiveSmallIntegerField
import json
#Post_Category        Product_Category


class SupporterDatasSerializer(views.APIView):     #important: you can use class SupporterDatasSerializer in view like: SupporterDatasSerializer().get(request, datas_selector='csrf_products_user') (returned value is Response type, you need .data to convert it as python dict(json)     
    '''
    /supporter_datas/products/ __________
    output = {"favorite_products": [...]}__________
    /supporter_datas/user/__________
    output = {"user": ...}__________
    /supporter_datas/csrf/__________
    output = {"csrfmiddlewaretoken":"...", "csrftoken": "..."}__________
    /supporter_datas/products_user_csrf/__________
    output = {"favorite_products": [...], "user": ..., "csrfmiddlewaretoken":"...", "csrftoken": "..."}
    '''
    def all_datas(self, request, **kwargs):
        datas = {}
        datas_selector = kwargs.get('datas_selector') if kwargs.get('datas_selector') else ''     
        if 'products' in datas_selector:
            datas = {**datas, **{'favorite_products': Cart(request).get_products()}}
        if 'user' in datas_selector:                                                    #if datas_selector was None it will raise error in here.
            userserializer = UserSerializer(request.user) if request.user.is_authenticated else UserSerializer()
            datas = {'user': userserializer.data}
        if 'csrf' in datas_selector:
            request_csrf_token, csrf_token= get_token(request), get_token(request) if "CSRF_COOKIE" not in request.META else ''
            datas = {**datas, **{'csrfmiddlewaretoken': get_token(request), 'csrftoken': get_token(request)}}
        return datas

    def get(self, request, *args, **kwargs):
        return Response(self.all_datas(request, **kwargs))
    
    def post(self, request, *args, **kwargs):
        return Response(self.all_datas(request, **kwargs))




from .mymethods import make_next
from django import forms
from django.forms.forms import DeclarativeFieldsMetaclass
from django.forms.models import BaseModelForm, ModelFormMetaclass
from django.forms.widgets import MediaDefiningClass
'''
class A(type):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class
class BBBBBBBBBBBBBB(metaclass=A):
    pass

class CCCCCCCCCCCCCCC(metaclass=A):
    pass
'''
class form1(BaseModelForm, metaclass=MediaDefiningClass):
    pass
      
def index(request):
    if request.method == 'GET':
        #cache.set('name', ['mkh is my name', 'akh is my name'])
        #str(request.META.get('HTTP_COOKIE'))id=14   fied_1=s2
        posts = type('loooooooooooooool', (form1,), {})
        print('@@@@@@@@@@@@@@@@@@@@@', posts)
        p = ''
        return render(request, 'app1/index.html', {'posts': posts, 'p': p})
    
    else:
        posts = myforms.RatingForm(request.POST)
        p = 'liiiiiil'
        return render(request, 'app1/index.html', {'posts': posts, 'p': p})




class HomePage(views.APIView): 
    def get(self, request, *args, **kwargs):
        '''
        output 6 last created product and 4 last created post(visible=True, and select products with available=True in first).
        '''
        products = get_products(0, 6)            
        posts = get_posts(0, 4)
        #supporter_datas = supporter_datas_serializer(request, mode='read')
        products_serialized = {'products': myserializers.ProductListSerializer(products, many=True, context={'request': request}).data}       #myserializers.ProductListSerializer(posts, many=True).data  is list not dict so cant use ** before it (like {**serialized})
        posts_serialized = {'posts': myserializers.PostListSerializer(posts, many=True, context={'request': request}).data}
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **products_serialized, **posts_serialized})

        



'''
@api_view(['GET', 'POST'])
def product_list(request):
    """
    List all products, or create a new product.
    """
    if request.method == 'GET':
        products = Product.objects.filter(id__lt=100).select_related('rating').prefetch_related('comments', 'image_set')
        serializer = myserializers.ProductDetailSerializer(products, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = myserializers.ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#.prefetch_related('comments__author')
class ProductList(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)
        serializer = p(queryset, many=True, context={'request': request})
        return Response(serializer.data)  
    queryset = Product.objects.filter(id__lt=100).select_related('rating').prefetch_related('comments', 'image_set')
    serializer_class = myserializers.ProductDetailSerializer
    #permission_classes = [permissions.IsAuthenticated]


why this desing expired?
class PostList(views.APIView):                                                              
    def get(self, request):
        count = 0
        posts = Post.objects.filter(id__in=[1, 2, 3, 4, 5])
        serializers = myserializers.PostListSerializer(posts, many=True, context={'request': request}).data              #you must put context={'request': request} in PostListSerializer argument for working request.build_absolute_uri  in PostListSerializer, otherwise request will be None in PostListSerializer and raise error 
        for post in posts:
            pk, slug = post.id, post.slug
            serializer = serializers[count]
            serializer['url'] = f'{pk}/{slug}/'
            #serializer['image_icon'] = request.build_absolute_uri(post.image_icon) 
            count += 1
        return Response(serializers)    

'''
    



class PostList(views.APIView):
    def get(self, request, *args, **kwargs):
        '''
        output 12 last created posts(visible=True)
        '''            
        posts = get_posts(0, 12)
        serializers = {'posts': myserializers.PostListSerializer(posts, many=True, context={'request': request}).data}             #you must put context={'request': request} in PostListSerializer argument for working request.build_absolute_uri  in PostListSerializer, otherwise request will be None in PostListSerializer and raise error 
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializers})   




class ProductList(views.APIView):
    def get(self, request, *args, **kwargs):
        '''
        output shown 24 last created product and 4 last created post(visible=True, and select products with available=True in first).
        '''        
        products = get_products(0, 24)    
        serializers = {'products': myserializers.ProductListSerializer(products, many=True, context={'request': request}).data}
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializers})




'''
output is same like ProductList(views.APIView) but can work without context={'request': request} initializing in serializer(ListAPIView put request auto).
class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(id__lt=100).select_related('rating')
    serializer_class = myserializers.ProductListSerializer
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True).data      
        return Response(serializer)
'''




class PostRootList(views.APIView):
    def get(self, request, *args, **kwargs):
        '''
        output all Post_Category objects.
        '''          
        post_roots = Root.objects.filter(post_product='post')
        serializers = {'post_roots': myserializers.RootListSerializer(post_roots, many=True).data}
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializers})




class ProductRootList(views.APIView):
    def get(self, request, *args, **kwargs):
        '''
        output all Product_Category objects.
        '''    
        product_roots = Root.objects.filter(post_product='product')
        serializers = {'product_roots': myserializers.RootListSerializer(product_roots, many=True).data}
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializers})



    
class PostDetail(views.APIView):
    def get(self, request, *args, **kwargs):                #dont need define like serializer = {'post': myserializers.PostDetailSerializer(product_roots).data} because myserializers.PostDetailSerializer(product_roots).data dont has many=True so is dict not list and dont raise error when putin in Reaponse
        '''
        input receive from /post_list/ like posts0.url = "3/یسشی/"__________
        output a post depend on pk you specify.
        '''
        #permission_classes = [permissions.IsAuthenticated]
        post = Post.objects.filter(id=kwargs['pk']).select_related('author').prefetch_related('contents', 'comment_set')
        serializer = myserializers.PostDetailSerializer(post).data
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializer})    




    
class ProductDetail(views.APIView):
    def get(self, request, *args, **kwargs):                #dont need define like serializer = {'post': myserializers.PostDetailSerializer(product_roots).data} because myserializers.PostDetailSerializer(product_roots).data dont has many=True so is dict not list and dont raise error when putin in Reaponse
        '''
        input receive from /product_list/ like products0.url = "1/گل-زر/"__________
        output a product depend on pk you specify.
        '''    
        product = Product.objects.filter(id=kwargs['pk']).select_related('rating').prefetch_related('comment_set', 'image_set')
        serializer = myserializers.ProductDetailSerializer(product[0]).data
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializer})




'''
generics.RetrieveAPIView
queryset = Post_Category.objects.all()
serializer_class = myserializers.PostListSerializer
def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = myserializers.PostListSerializer(instance.post_set.all(), many=True, context={'request': request})
    return Response(serializer.data)
'''



class ProductPostRootDetail(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):                #dont need define like serializer = {'post': myserializers.PostDetailSerializer(product_roots).data} because myserializers.PostDetailSerializer(product_roots).data dont has many=True so is dict not list and dont raise error when putin in Reaponse
        '''
        input: receive from /product_root_list/ or /post_root_list/  like product_roots0.url = "/1/زینتی/"__________
        output: Root is choicen depend on pk you specify and next depend on post or product root, will be shown all products or posts related to root and root's children. {"sessionid": "...", "products": [...]}
        '''    
        root = Root.objects.get(id=kwargs['pk'])
        if root.post_product == 'product':
            serializers = {'products': myserializers.ProductListSerializer(get_posts_products_by_roots, many=True, context={'request': request}).data}
        else:                      #root.post_product == 'post'
            serializers = {'posts': myserializers.PostListSerializer(get_posts_products_by_roots, many=True, context={'request': request}).data}            
        sessionid = request.session.session_key
        return Response({'sessionid': sessionid, **serializers})



    


