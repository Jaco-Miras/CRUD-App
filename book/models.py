from statistics import mode
from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=50)
    picture = models.ImageField()
    author = models.CharField(max_length=30, default='Guest')
    email = models.EmailField(blank=True)
    description = models.TextField(default='Available in Market')


    def __str__(self):
        return self.name