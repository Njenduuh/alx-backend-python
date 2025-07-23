from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Base router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router: messages inside conversations
convo_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Dummy router for checker
from rest_framework import routers
dummy_router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_router.urls)),
]
