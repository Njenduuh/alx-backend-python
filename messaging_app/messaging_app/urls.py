from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),       # Includes your app's routers
    path('api-auth/', include('rest_framework.urls')),  # Required for login/logout in browsable API
]
