from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('user/', include('accounts.urls')),
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
]
