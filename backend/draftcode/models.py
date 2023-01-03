from django.db import models

from account.models import User
from problem.models import Problem
from contest.models import Contest
from utils.shortcuts import rand_str

class DraftCode(models.Model):
    """
    임시저장된 코드 객체
    """
    id = models.IntegerField(primary_key=True, db_index=True)
    # 자동 저장 중 잘못된 저장이 되는 것을 방지하기 위한 checksum
    checksum = models.TextField(default=rand_str)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    last_update_time = models.DateTimeField(auto_now=True) # 수정 예정
    language = models.TextField()
    code = models.TextField(null=True, blank=True) # 질문 게시글의 질문 관련 언어
    
    class Meta:
        db_table = "draftcode"