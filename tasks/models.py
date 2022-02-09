from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from sqlalchemy import null 

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE , null=True,blank=True)
    priority = models.IntegerField(validators=[MinValueValidator(1)], null=True)

    def __str__(self):
        return self.title