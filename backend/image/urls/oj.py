from django.conf.urls import url

from ..views.admin import ImageUploadAPI

urlpatterns = [
    url(r"^upload_image_file/?$", ImageUploadAPI.as_view(), name="image_upload_api"),
]