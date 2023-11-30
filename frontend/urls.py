from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='front-home'), 
    path('frontend-about', views.about_page, name='front-about'),  
    path('register', views.register_page, name='front-register'), 
    path('login', views.login_page, name='front-login'), 
    path('logout', views.logout_page, name='front-logout'), 
]