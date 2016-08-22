from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=50)
    realName = models.CharField(max_length=100)
    index = models.CharField(max_length=7)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text

class User(models.Model):
    index = models.CharField(max_length=7)
    realName = models.CharField(max_length=100)
    path = models.CharField(max_length=25)
    sess_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.index
