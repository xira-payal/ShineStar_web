from django.urls import path
from . import views

cms_patterns = [
    path('view', views.carrer_page, name='carrer'), 
    path('add', views.add_carrer_page, name='addcarrer'),
    path('remove/<int:pk>/', views.delete_carrer_page, name='removecarr'),
    path('edit/<int:pk>/', views.update_carrer_page, name='editcarr')
]

urlpatterns = [
    path('frontend-carrer', views.carrer_pages, name='front-carrer'), 
    path('frontend-apply', views.apply_opening_page, name='front-apply'),
]  + cms_patterns

