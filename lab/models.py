from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClassRoom(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    subject = models.CharField(max_length=200)
    classname = models.CharField(max_length=10)
    students = models.ManyToManyField(User,related_name="participants",blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self) -> str:
        return self.subject+" "+self.classname

class Assignment(models.Model):
    class_in = models.ForeignKey(ClassRoom,on_delete=models.CASCADE)
    type = models.CharField(max_length=100,default="Question")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    due_date = models.DateField(blank=True)
    due_time = models.TimeField(default=False,blank=True)
    status = models.CharField(default='ongoing',max_length=20)
    question = models.TextField(max_length=500)

    class Meta:
        ordering = ['-updated', '-created']

class Answer(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_on']

class Poll(models.Model):
    assignment_in = models.ForeignKey(Assignment,on_delete=models.CASCADE,default=False)
    question = models.TextField(max_length=500)
    option_one = models.CharField(max_length=30,blank=True)
    option_two = models.CharField(max_length=30,blank=True)
    option_three = models.CharField(max_length=30,blank=True)
    option_four = models.CharField(max_length=30,blank=True)
    option_five = models.CharField(max_length=30,blank=True)
    option_one_count = models.IntegerField(default=-1)
    option_two_count = models.IntegerField(default=-1)
    option_three_count = models.IntegerField(default=-1)
    option_four_count = models.IntegerField(default=-1)
    option_five_count = models.IntegerField(default=-1)