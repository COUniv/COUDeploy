from importlib.metadata import requires
from django.db import models

class Banner(models.Model):
    banner = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=32, blank=True)
    isUse = models.BooleanField(default=False, blank=True)
    url = models.URLField(null=True, blank=True)
    
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    
class Using_banner(models.Model):
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    priority = models.IntegerField(null=True)
    url = models.URLField(null=True, blank=True)
    