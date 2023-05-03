from utils.api import serializers
from .models import CodeReview
class Test_serializers(serializers.ModelSerializer):
    class Meta:
        model = CodeReview
        fields = "__all__"