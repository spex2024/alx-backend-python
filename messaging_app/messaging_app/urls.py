from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/chats/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
