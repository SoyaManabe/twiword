from django.db import models

class Words(models.Model):
    NAME = 5
    VERB = 10

    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    tweet = models.CharField(max_length=200)
    word = models.CharField(max_length=200)
    trans = models.CharField(max_length=200)
    category = models.IntegerField(default=0)
    quiz = models.BooleanField(default=True)
    owner = models.CharField(max_length=200)

class Users(models.Model):
    screenName = models.CharField(max_length=50)
    userId = models.CharField(max_length=100)
