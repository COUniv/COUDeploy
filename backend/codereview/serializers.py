from utils.api import serializers
from .models import CodeReview, Review

class CodeReviewListSerializer(serializers.ModelSerializer):
    """
    코드 리뷰 게시글 목록 전송용
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = CodeReview
        exclude = ("last_update_time", "content", "writer")

class CodeReviewCreateSerializer(serializers.Serializer):
    """
    코드 리뷰 게시글 생성용
    """
    title = serializers.CharField()
    content = serializers.CharField()
    problemtype = serializers.CharField(allow_blank=True)
    problemid = serializers.CharField(allow_blank=True)

class CodeReviewSerializer(serializers.ModelSerializer):
    """
    코드 리뷰 게시글 detail용
    """
    class Meta:
        model = CodeReview
        exclude = ("id", "writer", "last_update_time")

class CodeReviewModifySerializer(serializers.Serializer):
    """
    코드 리뷰 게시글 수정용
    """
    title = serializers.CharField()
    content = serializers.CharField()
    id = serializers.IntegerField()

class ReviewListSerializer(serializers.Serializer):
    """
    댓글 출력용
    """
    class Meta:
        model = Review
        fields = '__all__'

class Test_serializers(serializers.ModelSerializer):
    class Meta:
        model = CodeReview
        fields = "__all__"