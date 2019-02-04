from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from unid import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('unid/', include('unid.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^search/autocomplete', views.autocomplete, name='autocomplete')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
