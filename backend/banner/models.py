from django.db import models

class Banner(models.Model):
    banner = models.TextField(null=True)
    title = models.CharField(max_length=32)
    
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)