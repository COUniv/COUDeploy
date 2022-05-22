from django.db import models

class Image(models.Model):
  id = models.IntegerField(primary_key=True, db_index=True)
  path = models.TextField(null=False)
  create_time = models.DateTimeField(auto_now_add=True)
  is_login_page = models.NullBooleanField()
  is_main_page = models.NullBooleanField()