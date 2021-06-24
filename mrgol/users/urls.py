from django.urls import path, include

from . import views


urlpatterns = [
    path('login/', views.LogIn.as_view(), name='loginview'),
    path('logout/', views.LogOut.as_view(), name='logoutview'),
    path('signup/', views.SignUp.as_view(), name='signupview'),
    path('userchange/', views.UserChange.as_view(), name='userchangeview'),
]

