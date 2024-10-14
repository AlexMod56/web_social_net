from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Chat(models.Model):
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f'{"Anonymous" if self.is_anonymous else self.author.username} - {self.timestamp}'
