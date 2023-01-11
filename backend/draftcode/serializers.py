from utils.api import serializers
from .models import DraftCode
from utils.serializers import LanguageNameChoiceField

class CreateDraftCodeSerializer(serializers.Serializer):
    problem_id = serializers.CharField(max_length=128)
    contest_id = serializers.IntegerField(required=False)
    language = LanguageNameChoiceField()


class DraftCodeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DraftCode
        fields = '__all__'

class UpdateDraftCodeSerializer(serializers.Serializer):
    problem_id = serializers.CharField(max_length=128)
    contest_id = serializers.IntegerField(required=False)
    language = LanguageNameChoiceField()
    id = serializers.IntegerField()
    checksum = serializers.CharField()
    code = serializers.CharField(max_length=1024 * 1024, allow_blank=True)

class DraftCodeSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftCode
        exclude = ("user", "contest", "problem", "last_update_time")

class DraftLastUpdatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DraftCode
        exclude = ("id", "user", "contest", "problem", "language", "checksum", "code")