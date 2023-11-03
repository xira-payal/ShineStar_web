from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name='b_login'), 
    path('register', views.registerPage, name='b_register'), 
    path('', views.homePage, name='home'), 
    path('logout', views.logoutPage, name='logout'), 
    path('forgotpassword', views.forgotPassword, name='forgotpassword'), 
]