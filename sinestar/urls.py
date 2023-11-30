from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    path('backend/', admin.site.urls),
    path('admin/', include('users.urls')),
    path('blog/', include('blog.urls')),
    path('carrer/', include('carrer.urls')),
    path('contact/', include('contact.urls')),
    path('opening/', include('opening.urls')),
    path('country/', include('country.urls')),
    path('', include('frontend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
