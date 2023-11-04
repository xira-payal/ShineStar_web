from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='front-home'), 
    path('frontend-about', views.about_page, name='front-about'), 
    path('frontend-carrer', views.carrer_page, name='front-carrer'), 
    path('frontend-contact', views.contact_page, name='front-contact'), 
    path('frontend-opening', views.opening_page, name='front-opening'),
    path('frontend-apply', views.apply_opening_page, name='front-apply'), 
    path('frontend-opening', views.opening_page, name='front-opening'), 
    path('register', views.register_page, name='front-register'), 
    path('login', views.login_page, name='front-login'), 
    path('logout', views.logout_page, name='front-logout'), 
]