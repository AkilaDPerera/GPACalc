from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=50)
    realName = models.CharField(max_length=100)
    index = models.CharField(max_length=7)
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.text