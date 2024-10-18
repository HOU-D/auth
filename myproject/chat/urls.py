from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, BlockViewSet, GameInviteViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'blocks', BlockViewSet)
router.register(r'invites', GameInviteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]