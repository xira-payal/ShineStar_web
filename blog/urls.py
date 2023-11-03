from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.blog_page, name='blog'), 
    path('add/', views.add_blog_page, name='addblog'),
    path('edit/<int:pk>/', views.update_blog_page, name='editblog'),
    path('remove/<int:pk>/', views.delete_blog_page, name='removeblog'),
    path('go_back/', views.go_back, name='go_back'),
]