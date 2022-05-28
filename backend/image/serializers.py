from utils.api import serializers
from .models import Image
from django import forms


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ("id", "is_login_page", "is_main_page")

class ImageUploadForm(forms.Form):
    image = forms.FileField()
    