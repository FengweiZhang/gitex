from django.db import models
class Message(models.Model):
    title = models.CharField(max_length=100,default='Please write your title here...')
    content = models.TextField(blank=True,default='Please write something here...')
    asker = models.CharField(max_length=100,default='Anonymous users')
# Create your models here.
