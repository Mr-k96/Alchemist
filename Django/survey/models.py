# models.py
from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)