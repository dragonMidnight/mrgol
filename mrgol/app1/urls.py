from django.urls import path, include
from rest_framework import routers


from . import views

'''            
router = routers.DefaultRouter()
router.register(r'', views.ProductViewSet)
    path('viewset/', include(router.urls), name='product_viewset'),'''



urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('index/', views.index, name='index'),
    path('post_list/', views.PostList.as_view(), name='post_list'),
    path('product_list/', views.ProductList.as_view(), name='product_list'),
    path('post_root_list/', views.PostRootList.as_view(), name='post_root_list'),
    path('product_root_list/', views.ProductRootList.as_view(), name='product_root_list'),
    path('product_post_root_detail/<pk>/<slug>/', views.ProductPostRootDetail.as_view(), name='product_post_root_detail'),
    path('post_detail/<pk>/<slug>/', views.PostDetail.as_view(), name='post_detail'),   #slug here dont affect class PostDetail for query(only query on pk for retriving posts)    
    path('product_detail/<pk>/<slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('supporter_datas/<datas_selector>/', views.SupporterDatasSerializer.as_view(), name='support_datas_serialized'),

]

