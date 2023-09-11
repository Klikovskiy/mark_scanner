from django.contrib import admin
from django.urls import path, include

from scanner_user.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('scanner_auth.urls')),
    path('', HomeView.as_view(), name='home'),
]
