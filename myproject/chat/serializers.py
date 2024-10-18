from rest_framework import serializers
from .models import Message, Block, GameInvite
from user_management.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']

class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ['id', 'blocker', 'blocked']

class GameInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameInvite
        fields = ['id', 'sender', 'recipient', 'status', 'timestamp']