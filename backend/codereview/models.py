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
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.TextField(null=False)
    
    title = models.CharField(max_length=40, null=True)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    
    review_count = models.PositiveIntegerField(default=0)
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
    username = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    
    target = models.ForeignKey(CodeReview, on_delete=models.CASCADE)
    content = models.TextField(null=False)

    line_num = models.PositiveIntegerField(default = -1, null=True) #타겟 라인 넘버
    is_comment_writer = models.NullBooleanField()
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")