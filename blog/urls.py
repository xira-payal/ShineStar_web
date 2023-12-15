from django.urls import path
from . import views

cms_patterns = [
    path('view/', views.blog_page, name='blog'), 
    path('add/', views.add_blog_page, name='addblog'),
    path('edit/<int:pk>/', views.update_blog_page, name='editblog'),
    path('remove/<int:pk>/', views.delete_blog_page, name='removeblog'),
]

urlpatterns = [
    # path('blog_view/<slug:slug>/', views.blog_view, name='frontblog'), 
] + cms_patterns

