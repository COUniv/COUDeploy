from django.db import models
from utils.models import JSONField

from account.models import User
from contest.models import Contest
from utils.models import RichTextField
from utils.constants import Choices

from django.contrib.postgres.fields import ArrayField


class ProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "problem_tag"


class ProblemRuleType(Choices):
    ACM = "ACM"
    OI = "OI"


class ProblemDifficulty(object):
    Level1 = "Level1"
    Level2 = "Level2"
    Level3 = "Level3"
    Level4 = "Level4"
    Level5 = "Level5"
    Level6 = "Level6"
    Level7 = "Level7"
    Level8 = "Level8"
    Level9 = "Level9"
    Level10 = "Level10"
    Level11 = "Level11"
    Level12 = "Level12"
    Level13 = "Level13"
    Level14 = "Level14"
    Level15 = "Level15"
    # High = "High"
    # Mid = "Mid"
    # Low = "Low"


class ProblemIOMode(Choices):
    standard = "Standard IO"
    file = "File IO"


def _default_io_mode():
    return {"io_mode": ProblemIOMode.standard, "input": "input.txt", "output": "output.txt"}


class Problem(models.Model):
    # display ID
    _id = models.TextField(db_index=True)
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    # for contest problem
    is_public = models.BooleanField(default=False)
    title = models.TextField()
    # HTML
    description = RichTextField()
    input_description = RichTextField()
    output_description = RichTextField()
    # [{input: "test", output: "123"}, {input: "test123", output: "456"}]
    samples = JSONField()
    test_case_id = models.TextField()
    # [{"input_name": "1.in", "output_name": "1.out", "score": 0}]
    test_case_score = JSONField()
    hint = RichTextField(null=True)
    languages = JSONField()
    template = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)
    # we can not use auto_now here
    last_update_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # ms
    time_limit = models.IntegerField()
    # MB
    memory_limit = models.IntegerField()
    # io mode
    io_mode = JSONField(default=_default_io_mode)
    # special judge related
    spj = models.BooleanField(default=False)
    spj_language = models.TextField(null=True)
    spj_code = models.TextField(null=True)
    spj_version = models.TextField(null=True)
    spj_compile_ok = models.BooleanField(default=False)
    rule_type = models.TextField()
    visible = models.BooleanField(default=True)
    difficulty = models.TextField()
    tags = models.ManyToManyField(ProblemTag)
    source = models.TextField(null=True)
    # for OI mode
    total_score = models.IntegerField(default=0)
    submission_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)
    # {JudgeStatus.ACCEPTED: 3, JudgeStaus.WRONG_ANSWER: 11}, the number means count
    statistic_info = JSONField(default=dict)
    share_submission = models.BooleanField(default=False)

    class Meta:
        db_table = "problem"
        unique_together = (("_id", "contest"),)
        ordering = ("create_time",)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    def add_ac_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save(update_fields=["accepted_number"])

    def getDifficultyToWeightValue(self):
        diff = self.difficulty
        slice_dif = diff[5:]
        dif_to_int = int(slice_dif)
        #wexp weight value = 1 - (4-difficulty)/15
        exp_weight_value = 1 - (4 - dif_to_int) / 15
        return exp_weight_value

class ProblemCategory(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    title = models.TextField()
    description = RichTextField()
    problems = ArrayField(models.IntegerField(), blank=True, default=list)
    # 작성자, 작성 시각, visible 등

class ProblemCategoryList(models.Model):
    categories = ArrayField(models.TextField(), blank=True, default=list)

class ProblemRating(models.Model):
    rating =  ArrayField(ArrayField(models.FloatField(), blank=True, default=list), blank=True, default=list)
    update_expire_time = models.DateTimeField(null=True)