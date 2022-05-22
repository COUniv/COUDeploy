from utils.api import serializers
from .models import Image

class ImageListSerializer(serializers.ModelSericalizer):
    class Meta:
        model = Image
        fields = "__all__"

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ("id", "is_login_page", "is_main_page")