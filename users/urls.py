from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name='admin_login'), 
    path('', views.homePage, name='admin_home'), 
    path('logout', views.logoutPage, name='admin_logout'),
    path('profile', views.profilePage, name='admin_profile'),
    path('changePassword', views.changePassword, name='admin_changePassword'),
    path('forgotPassword', views.forgot_password, name='admin_forgotPassword'),
    path('resetPassword/<str:token_b64>/', views.reset_password, name='admin_resetPassword'),
]
