from django.db import models

class Student(models.Model):
    date = models.DateTimeField(auto_now=True)
    
    index = models.CharField(max_length=7, unique=True)
    realName = models.CharField(max_length=100)
    cookie = models.CharField(max_length=100, unique=True)
    
    lastTry = models.SmallIntegerField()

    count = models.IntegerField()
    overallGPA = models.DecimalField(max_digits=6, decimal_places=4)
    performance = models.TextField() #{semNo:[(moduleID,grade),(),(),()],}
    semGPA = models.TextField() #{semNo:3.5, semNo:3.7}
    
    def __repr__(self):
        return self.index


class Module(models.Model):
    moduleName = models.CharField(max_length=100)
    moduleCode = models.CharField(max_length=10, unique=True)
    credit = models.CharField(max_length=4)
    semester = models.CharField(max_length=30)
    
    def __repr__(self):
        return self.moduleName

