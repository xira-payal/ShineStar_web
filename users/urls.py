from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name='admin_login'), 
    path('', views.homePage, name='admin_home'), 
    path('logout', views.logoutPage, name='admin_logout'), 
]