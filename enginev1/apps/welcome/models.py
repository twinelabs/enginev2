from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)

    prefs_color_bg = models.CharField(max_length=100, blank=True)
    prefs_color_sidebar = models.CharField(max_length=100, blank=True)
    prefs_color_accent = models.CharField(max_length=100, blank=True)

    logo = models.ImageField(blank=True, null=True, upload_to='./img/logos/')

    class Meta:
        app_label = 'welcome'

    def __str__(self):
        return self.company_name
