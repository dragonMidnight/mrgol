from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.sessions.backends.db import SessionStore

from rest_framework import views
from rest_framework.response import Response
from rest_framework import permissions, authentication

from .myserializers import Test4Serializer, Test3Serializer, UserSerializer, UserChangeSerializer
from .mymethods import login_validate
from app1.views import SupporterDatasSerializer
from app1.models import Test3
from cart.models import SesKey
from cart.cart import Cart
from customed_files.rest_framework.rest_framework_customed_classes.custom_rest_authentication import CustomSessionAuthentication 




class LogIn(views.APIView):
    def get(self, request, *args, **kwargs):                           #maybe an authenticated user come to login.get page, so we should provide sessionid
        '''
        input in header cookie "" or "favorite_products_ids=1,2,3"
        output {"csrfmiddlewaretoken": "...",  "csrftoken": "..."}
        '''
        return Response({**SupporterDatasSerializer().get(request, datas_selector='csrf').data})              #dont need sending product or other, supose user request several time this page(refreshing page), why in every reqeust, send products and other, for optain product front can request to other link and optain it and save it and in refreshing page dont need send products again(cach it in user browser).

    def post(self, request, *args, **kwargs):                            #an example for acceesing to LogIn.post:   http POST http://192.168.114.6:8000/users/login/ email=a@gmail.com password=a13431343 csrfmiddlewaretoken=jKnAefVUhdxR0fS3Jh0uozdtBc3FwtDOy2ghKVucLG479jQMYFTSxxIpjVjEEkds cookie:"csrftoken=uBvlhHOgqfaYmASnY3BtanycxOKz00cVJTo2NnnyUIHevEQ6druRjl38fx0y8RMz; favorite_products_ids=1,3,4"        
        '''
        input in request.POST {"csrfmiddlewaretoken": "...",  "email": "...", "password": "..."}
        input in header cookie "csrftoken=..." or "csrftoken=...; favorite_products_ids=1,2,3;" if favorite_products_ids provides(in user cookie)
        output  {"sessionid": "...",  "user": "...", "favorite_products_ids": "..."}     "favorite_products_ids=1,2,3"
        '''
        user = login_validate(request)
        CustomSessionAuthentication().enforce_csrf(request)          #if you dont put this here, we will havent csrf check (meants without puting csrf codes we can login easily)(because in djangorest, csrf system based on runing class SessionAuthentication(here)CustomSessionAuthentication and class CustomSessionAuthentication runs when you are loged in, because of that we use handy method enforce_csrf(we arent here loged in), just in here(in other places, all critical tasks that need csrf checks have permissions.IsAuthenticated require(baese csrf check mishavad)).
        login(request, user)

        cart = Cart(request)
        seskey_obj = SesKey.objects.get(user=self.request.user)
        cart_products_ids_insession = SessionStore(session_key=seskey_obj.ses_key).get('cart_products_ids')  
        cart_products_ids_insession = cart_products_ids_insession if cart_products_ids_insession else []  
        cart_products_ids_incookie = cart.ids
        [cart_products_ids_incookie.remove(i) for i in cart_products_ids_insession if i in cart_products_ids_incookie]
        cart_products_ids = cart_products_ids_insession + cart_products_ids_incookie                                       #supose user adds some products to its favorite list when was logout and now want login, so that products ids that is in his vookie should sum with his ids in session.
        cart.ids = cart_products_ids
        supporter_datas = SupporterDatasSerializer().get(request, datas_selector='user').data                     
        
        return Response({'sessionid': request.session.session_key, **supporter_datas, 'favorite_products_ids': cart_products_ids})   #important: front must set favorite_products_ids to user cooie as name expected in cart.cart.Cart, supporter_datas['favorite_products'] or cart.get_products use user cookie (request.COOKIES.get('favorite_products_ids')) so it must be updated here to be work truly other methods.
       



class LogOut(views.APIView):
    '''
    input = in header cookie "sessionid=..."__________
    output = {"user": "..."}__________
    note, deleting user cookie should done(by front) after logout.
    '''
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        seskey_obj = SesKey.objects.get(user=self.request.user)
        if request.POST.get('favorite_products_ids'):
            cartsession = SessionStore(session_key=seskey_obj.ses_key) 
            cartsession['cart_products_ids'] = Cart(request).ids
            cartsession.save()
        logout(request)
        return Response(SupporterDatasSerializer().get(request, datas_selector='user').data)   


#serializers.ValidationError('hiiiiiiiiiiiiiiiiiii')
from rest_framework import serializers
from app1.models import Test3
from rest_framework.exceptions import ErrorDetail, ValidationError, ErrorDetail
class SignUp(views.APIView):
    def get(self, request, *args, **kwargs):
        '''
        output = {"csrfmiddlewaretoken": "...",  "csrftoken": "..."}
        '''
        #email, password1, password2 = request.GET.get('email'), request.GET.get('password1'), request.GET.get('password2')
        ##'email':'', 'password': password1, 'password2': password2
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        serializer = Test4Serializer(data={'field_1': 'aaaaaaa'})
        serializer.is_valid(raise_exception=True)
        return Response({})       
        #return Response({**SupporterDatasSerializer().get(request, datas_selector='csrf').data})

    def post(self, request, *args, **kwargs):
        '''
        input in POST = {"csrfmiddlewaretoken": "...", "email": "...", "password1": "...", "password2": "..."}__________
        input in header = {"csrftoken": "..."}
        '''
        CustomSessionAuthentication().enforce_csrf(request)
        email, password1, password2 = request.POST.get('email'), request.POST.get('password1'), request.POST.get('password2')
        serializer = UserSerializer(data={'email':email, 'password1': password1, 'password2': password2})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer)

    


class UserChange(views.APIView):
    def get(self, request, *args, **kwargs):
        '''
        input, output = None__________
        method get is done in front, front create a userchangeform and request url /supporter_datas/user/ to optain user datas for prepopulate fields.__________
        for decide which user fields should provide in userchangeform, you can see User table in /static/app1/mrgol_visualized.png/
        '''
        return Response()
    
    def put(self, request, *args, **kwargs):
        '''
        input = submited userchangeform should sent here (/userchange/) like <from action="domain.com/users/userchange/" ...>__________
        output(in success) = front should request user (/supporter_datas/user/) to optain user with new changes.__________
        output(in failure) = {"is_superuser": ["Must be a valid boolean."],"email": ["Enter a valid email address."]}
        '''
        serializer = UserChangeSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer)

        
