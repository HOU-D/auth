# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=100, unique=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    friends= models.ManyToManyField('self',symmetrical=True,blank=True)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    energie_point = models.IntegerField(default=5)
    skill_point =models.IntegerField(default=100)

class Match(models.Model):
  player1 = models.ForeignKey(CustomUser, related_name='matches_as_player1', on_delete=models.CASCADE)
  player2 = models.ForeignKey(CustomUser, related_name='matches_as_player2', on_delete=models.CASCADE)
  winner = models.ForeignKey(CustomUser, related_name='matches_won', on_delete=models.CASCADE, null=True, blank=True)
  date_played = models.DateTimeField(auto_now_add=True)
  player1_score = models.IntegerField(default=0)
  player2_score = models.IntegerField(default=0)
  score = models.CharField(max_length=10, blank=True, null=True)

# /api/v1/match/[username] -> return all the games that 