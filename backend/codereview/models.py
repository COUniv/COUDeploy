from django.db import models
from account.models import User
from problem.models import Problem
from django.conf import settings
from django.contrib.postgres.fields import ArrayField  

class Code(models.Model):
    '''
    코드 관리를 위한 1:1 테이블 객체
    '''
    origin = models.TextField(null=True)
    code = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    # 추가?

class CodeReview(models.Model):
    """
    코드 리뷰 갤러리 객체
    """
    id = models.IntegerField(primary_key=True, db_index=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.TextField(null=False)
    
    title = models.CharField(max_length=40, null=True)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    
    comment_count = models.PositiveIntegerField(default=0)
    #problemid = models.TextField(null=True, blank=True) # 해당 문제 아이디
    
    code = models.OneToOneField(Code, on_delete=models.CASCADE)
    #problem = models.ForeignKey(Problem, null=True)    #관련 문제
    
    class Meta:
        db_table = "codereview"
        ordering = ("-create_time",)

class Review(models.Model):
    """
    리뷰 테이블 객체
    """
    articleid = models.IntegerField()
    username = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    
    target = models.ForeignKey(CodeReview, on_delete=models.CASCADE)
    content = models.TextField(null=False)

    line_num = models.PositiveIntegerField(default = -1, null=True) #타겟 라인 넘버
    is_comment_writer = models.NullBooleanField()
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")

class CodeReviewNotificationType(object):
    """
    알림 타입 객체
    """
    LIKE = "LIKE"
    COMMENT = "COMMENT"

class CodeReviewNotification(models.Model):
    """
    알림 객체
    """
    #id = models.IntegerField(primary_key=True, db_index=True) # 알림 고유 ID
    create_time = models.DateTimeField(auto_now_add=True) # 알림 생성 시각
    read_time = models.DateTimeField(null=True) # 알림 읽은 시각
    is_read = models.BooleanField(default=False) # 알림 읽기 여부
    url = models.TextField(null=False) # 알림이 발생한 경로
    target_username = models.TextField(null=False) # 알림을 받는 회원 이름
    action_username = models.TextField(null=False) # 알림을 생성한 회원 이름
    notificationtype = models.TextField(null=False) # 알림 타입 - 댓글 / 좋아요
    content = models.TextField(null=False) # 알림 내용
    comment_content = models.TextField(null=True) # Comment일 경우 content를 담아둠