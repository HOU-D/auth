from django.db import models
from user_management.models import CustomUser

class Message(models.Model):
    sender = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sent_message')
    receiver = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='receive_message')
    content = models.TimeField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

class BLock(models.Model):
    blocker =models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blocking')
    blocked = models.ForeignKey(CustomUser,on_delete=models.CASCADE, related_name='blocked')

class Gameinvite(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='sent_invite')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='receive_invite')
    status = models.CharField(max_length=10, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('declined', 'Declined')))
    timestamp = models.DateTimeField(auto_now_add=True)
