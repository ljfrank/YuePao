from django.db import models

class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    isAdmin = models.BooleanField()
    phone = models.CharField(max_length=20)
