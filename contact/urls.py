from django.urls import path
from . import views

urlpatterns = [
    path('view/', views.contact_page, name='contact'), 
    path('add/', views.add_contact_page, name='addcontact'),
    path('edit/<int:pk>/', views.update_contact_page, name='editcontact'),
    path('remove/<int:pk>/', views.delete_contact_page, name='removecontact'),
]