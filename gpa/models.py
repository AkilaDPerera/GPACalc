from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User)
    
    fullName = models.CharField(max_length = 100)
    count = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return str(self.user) + " : " + str(self.count)
    
    def __str__(self):
        return str(self.user) + " : " + str(self.count)
    

class Module(models.Model):
    moduleCode = models.CharField(max_length=10, primary_key=True)
     
    moduleName = models.CharField(max_length=100)
    credit = models.CharField(max_length=4)
    
    def __repr__(self):
        return self.moduleName
    
    def __str__(self):
        return self.moduleCode + " : " +self.moduleName

class Semester(models.Model):
    semesterName = models.CharField(max_length=100)
    
    def __repr__(self):
        return self.semesterName
    
    def __str__(self):
        return self.semesterName

class Feedback(models.Model):
    user = models.ForeignKey(User)
    
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return self.user + " : " + self.message
    
    def __str__(self):
        return self.user + " : " + self.message
    
class Performance(models.Model):
    user = models.ForeignKey(User)
    module = models.ForeignKey(Module)
    semester = models.ForeignKey(Semester)
    
    grade = models.CharField(max_length=8, default='UNKNOWN')
    date = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
        return str(self.user) + " : " + str(self.module) + " : " + str(self.grade)
    
    def __str__(self):
        return  str(self.user) + " : " + str(self.module) + " : " + str(self.grade)
    

