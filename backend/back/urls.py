from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ecopatrol/', include('djoser.urls')),
    path('api/ecopatrol/', include('djoser.urls.authtoken')),
    path('api/ecopatrol/', include('apps.person.urls')),
    path('api/phone/', include('apps.phone.urls')),
    path('api/legalization/', include('apps.legalization.urls')),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
