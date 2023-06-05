# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Reccords (models.Model):
    time = models.CharField(max_length=100, null=True, blank=True ,default="")
    count = models.IntegerField(null=True, default=0)
    location = models.CharField(max_length=100, null=True, default="Location Not Found")
    user = models.CharField(max_length=100, null=True, default="User Not Found")
