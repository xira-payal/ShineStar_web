from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='Front_Home'), 
    path('frontend_about', views.about_page, name='Front_about'), 
    path('frontend_carrer', views.carrer_page, name='Front_carrer'), 
    path('frontend_contact', views.contact_page, name='Front_contact'), 
    path('frontend_opening', views.opening_page, name='Front_opening'),
    path('frontend_apply', views.apply_opening_page, name='Front_apply'), 
    path('frontend_opening', views.opening_page, name='Front_opening'), 
    path('register', views.register_page, name='Front_register'), 
    path('login', views.login_page, name='Front_login'), 
    path('logout', views.logout_page, name='Front_Logout'), 
]