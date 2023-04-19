from django.db import models
from uuid import uuid4

class Notification(models.Model):
    slug = models.CharField(max_length=100, default=uuid4)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=2000)
    type  = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True, default='')
    issued_date =  models.DateTimeField(blank=True)


    class Meta:
        ordering = ['-issued_date',]


    def __str__(self):
        return self.title