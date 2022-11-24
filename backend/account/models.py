from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.db import models
from utils.models import JSONField
from django.contrib.postgres.fields import ArrayField  

class AdminType(object):
    REGULAR_USER = "Regular User"
    ADMIN = "Admin"
    SUPER_ADMIN = "Super Admin"


class ProblemPermission(object):
    NONE = "None"
    OWN = "Own"
    ALL = "All"


class UserManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        return self.get(**{f"{self.model.USERNAME_FIELD}__iexact": username})


class User(AbstractBaseUser):
    username = models.TextField(unique=True)
    email = models.TextField(null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True)

    # One of UserType
    admin_type = models.TextField(default=AdminType.REGULAR_USER)
    problem_permission = models.TextField(default=ProblemPermission.NONE)
    reset_password_token = models.TextField(null=True)
    reset_password_token_expire_time = models.DateTimeField(null=True)
    # SSO auth token
    auth_token = models.TextField(null=True)
    two_factor_auth = models.BooleanField(default=False)
    tfa_token = models.TextField(null=True)
    session_keys = JSONField(default=list)
    # open api key
    open_api = models.BooleanField(default=False)
    open_api_appkey = models.TextField(null=True)
    is_disabled = models.BooleanField(default=False)

    is_email_verify = models.BooleanField(default=False)
    verify_email_token = models.TextField(null=True)
    verify_email_token_expire_time = models.DateTimeField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    problem_sequence = ArrayField(models.TextField(null=True), blank=True, default=list)
    grass = ArrayField(models.DateTimeField(), blank=True, default=list)

    last_activity = models.DateTimeField(null=True)

    objects = UserManager()

    def is_admin(self):
        return self.admin_type == AdminType.ADMIN

    def is_super_admin(self):
        return self.admin_type == AdminType.SUPER_ADMIN

    def is_admin_role(self):
        return self.admin_type in [AdminType.ADMIN, AdminType.SUPER_ADMIN]

    def can_mgmt_all_problem(self):
        return self.problem_permission == ProblemPermission.ALL

    def is_contest_admin(self, contest):
        return self.is_authenticated and (contest.created_by == self or self.admin_type == AdminType.SUPER_ADMIN)
    
    class Meta:
        db_table = "user"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # acm_problems_status examples:
    # {
    #     "problems": {
    #         "1": {
    #             "status": JudgeStatus.ACCEPTED,
    #             "_id": "1000"
    #         }
    #     },
    #     "contest_problems": {
    #         "1": {
    #             "status": JudgeStatus.ACCEPTED,
    #             "_id": "1000"
    #         }
    #     }
    # }
    acm_problems_status = JSONField(default=dict)
    # like acm_problems_status, merely add "score" field
    oi_problems_status = JSONField(default=dict)

    real_name = models.TextField(null=True)
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")
    blog = models.URLField(null=True)
    mood = models.TextField(null=True)
    github = models.TextField(null=True)
    school = models.TextField(null=True)
    major = models.TextField(null=True)
    language = models.TextField(null=True)
    # for ACM
    accepted_number = models.IntegerField(default=0)
    accepted_of_all_submission_number = models.IntegerField(default=0) # 총 통과한 제출 수
    # for OI
    total_score = models.BigIntegerField(default=0)
    submission_number = models.IntegerField(default=0)
    # for rating score
    rating_score = models.FloatField(default=0)
    rating_position = ArrayField(ArrayField(models.FloatField(), blank=True, default=list), blank=True, default=list)

    def add_accepted_of_all_submission_problem_number(self):
        self.accepted_of_all_submission_number = models.F("accepted_of_all_submission_number") + 1
        self.save()
        
    def add_accepted_problem_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save()

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save()

    # 총점을 계산할 때 먼저 문제의 이전 점수를 뺀 다음 현재 점수를 더해야 함.
    def add_score(self, this_time_score, last_time_score=None):
        last_time_score = last_time_score or 0
        self.total_score = models.F("total_score") - last_time_score + this_time_score
        self.save()

    def update_rating(self, user):
        from problem.models import Problem
        profile = user.userprofile
        acm_problems = profile.acm_problems_status.get("problems", {})
        accepted_ids = []
        result = []
        for acm_problem_key in list(acm_problems.keys()):
            if acm_problems[acm_problem_key]["status"] == 0 or acm_problems[acm_problem_key]["status"] == "0":
                accepted_ids.append(acm_problem_key)
        accepted_ids = list(accepted_ids)
        accepted_problem_list = Problem.objects.filter(id__in=accepted_ids)
        total_size = accepted_problem_list.count()
        rating = 0
        if total_size == 0:
            result.append([0, 0])
            self.rating_position = result
        else:
            for problem in accepted_problem_list:
                #wexp weight value = 1 - (4-difficulty)/15
                exp = problem.getDifficultyToWeightValue()

                '''
                rating = sum(accepted_problems + (accepted_problems ** (1 - (4-difficulty) / 15) / 15)) / accepted_problems
                '''
                rating += (total_size + ((total_size ** exp) / 15))
            rating = rating / total_size
            result.append([total_size, rating])
            self.rating_position = result
        self.rating_score = rating
        self.save()

    class Meta:
        db_table = "user_profile"

class ManagedUserList(models.Model):
    """
    관리자에 의해 관리되는 유저 리스트
    """
    id = models.IntegerField(primary_key=True, db_index=True) # 메니지 리스트 고유 ID
    # 해당 계정이 삭제될 경우에도 유지하도록 함(수정 권한 -> SuperAdmin으로 변경될 예정)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=128, null=True)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)

    users = models.ManyToManyField(User, related_name='managed_lists', null=True, blank=True)

    class Meta:
        db_table = "manged_user_list"
        ordering = ("-last_update_time",)