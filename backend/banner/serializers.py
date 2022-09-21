from utils.api import serializers
from django import forms
from .models import *

class BannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"

class UsingBannerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Using_banner
        fields = "__all__"

class ImageUploadForm(forms.Form):
    image = forms.FileField()
    #title = forms.CharField()

