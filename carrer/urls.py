from django.urls import path
from . import views

urlpatterns = [
    path('view', views.carrer_page, name='carrer'), 
    path('add', views.add_carrer_page, name='addcarrer'),
    path('remove/<int:pk>/', views.delete_carrer_page, name='removecarr'),
    path('edit/<int:pk>/', views.update_carrer_page, name='editcarr')
]