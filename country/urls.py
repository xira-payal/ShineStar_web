from django.urls import path
from . import views

cms_patterns = [
    path('view/', views.country_page, name='country'), 
    path('add/', views.add_country_page, name='addcountry'),
    path('edit/<int:pk>/', views.update_country_page, name='editcountry'),
    path('remove/<int:pk>/', views.delete_country_page, name='removecountry'),
]

urlpatterns = [] + cms_patterns

