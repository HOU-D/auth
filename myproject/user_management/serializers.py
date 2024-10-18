# serializers.py
from rest_framework import serializers
from .models import CustomUser
from .models import Match
from django.db import IntegrityError
from django.db import IntegrityError 

class UserSerializer(serializers.ModelSerializer):
  class Meta:
      model = CustomUser
      fields = ['id', 'username', 'display_name', 'avatar', 'wins', 'losses', 'last_active','energie_point' ,'energie_point']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'confirm_password', 'display_name', 'avatar']

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        try:
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                display_name=validated_data.get('display_name', ''),
                avatar=validated_data.get('avatar', None)
            )
            return user
        except IntegrityError as e:
            raise serializers.ValidationError({"detail": "Username or password exists."})

class MatchSerializer(serializers.ModelSerializer):
  class Meta:
      model = Match
      fields = ['id', 'player1', 'player2', 'winner', 'score', 'date_played']
