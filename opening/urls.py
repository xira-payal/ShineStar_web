from django.urls import path
from . import views

cms_patterns = [
    path('view/', views.opening_page, name='opening'), 
    path('add/', views.add_opening_page, name='addopening'),
    path('edit/<int:pk>/', views.update_opening_page, name='edit'),
    path('remove/<int:pk>/', views.delete_opening_page, name='remove'),
]

urlpatterns = [
    path('frontend-opening', views.opening_pages, name='front-opening'),
] + cms_patterns