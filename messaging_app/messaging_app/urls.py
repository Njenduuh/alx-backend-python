from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),           # ✅ Include your chats routes under /api/
    path('api-auth/', include('rest_framework.urls')),  # ✅ Needed for browsable API login/logout
]
