from rest_framework import viewsets
from .models import Message, Block, GameInvite
from .serializers import MessageSerializer, BlockSerializer, GameInviteSerializer
from rest_framework.permissions import IsAuthenticated
from user_management.models import CustomUser

class MessageViewSet(viewsets.ModelviewSet):
    serializer_class = MessageSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        return GameInvite.objects.filter(
            receiver= self.request.user
        ) | GameInvite.objects.filter(
            sender = self.request.user
        )
    def perform_create(self,serializer):
        serializer.save(sender=self.request.user)

class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = BlockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Block.objects.filter(blocker=self.request.user)

    def perform_create(self, serializer):
        serializer.save(blocker=self.request.user)

class GameInviteViewSet(viewsets.ModelViewSet):
    serializer_class = GameInviteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GameInvite.objects.filter(
            receiver=self.request.user
        ) | GameInvite.objects.filter(
            sender=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
