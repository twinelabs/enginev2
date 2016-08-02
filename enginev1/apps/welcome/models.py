from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    domain_prefix = models.CharField(max_length=100, blank=True)
    alpha_label = models.CharField(max_length=100, blank=True)
    beta_label = models.CharField(max_length=100, blank=True)
    alpha_lastupdate = models.DateTimeField(blank=True, null=True)
    beta_lastupdate = models.DateTimeField(blank=True, null=True)

    logo = models.ImageField(blank=True, null=True)

    class Meta:
        app_label = 'welcome'

    def __str__(self):
        return self.name
