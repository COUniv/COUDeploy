from datetime import timezone
from ..models import DraftCode, Problem, User
from utils.api import APIView, validate_serializer
from ..serializers import UpdateDraftCodeSerializer, DraftCodeSafeSerializer, CreateDraftCodeSerializer
from account.decorators import login_required
from django.db.models import Q

class DraftCodeAPI(APIView):

    @validate_serializer(CreateDraftCodeSerializer)
    @login_required
    def post(self, request):
        data = request.data
        try:
            problem = Problem.objects.get(id=data["problem_id"], contest_id=data.get("contest_id"), visible=True)
        except Problem.DoesNotExist:
            return self.error("존재하지 않은 문제입니다")
        draft = DraftCode.objects.create(user=request.user, problem=problem, contest=data.get("contest_id"), language=data["language"])
        draft.save()

    @login_required
    def get(self, request):
        # contest 는 별도 api로 반환
        if not request.GET.get("problem_id"):
            return self.error("Invalid Parameter")
        if not request.GET.get("language"):
            return self.error("Invalid Parameter")

        problem_id = request.GET.get("problem_id")
        language = request.GET.get("language")

        drafts = DraftCode.objects.filter(user=request.user)
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id__isnull=True, visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            try:
                draft = drafts.get(problem=problem, language=language)
            except DraftCode.DoesNotExist:
                return self.success("None")
            result = DraftCodeSafeSerializer(draft).data
            return self.success(result)

    # contest는 별도 api가 관여
    @validate_serializer(UpdateDraftCodeSerializer)
    @login_required
    def put(self, request):
        data = request.data
        id = data["id"]
        checksum = data["checksum"]
        if not data["code"]:
            return self.success()

        problem_id = data["problem_id"]
        if data["contest_id"]:
            return self.error("대회 문제가 아닙니다")
        language = data["language"]
        code = data["code"]
        drafts = DraftCode.objects.filter(user=request.user)
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id__isnull=True, visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            try:
                draft = drafts.get(problem=problem, language=language)
            except DraftCode.DoesNotExist:
                return self.success("임시저장이 존재하지 않습니다")
            if draft.id == id and draft.checksum == checksum:
                draft = DraftCode.objects.get(id=id, checksum=checksum)
                draft.code = code
                draft.save()
                return self.success(draft.last_update_time)
            return self.error("Invalid checksum")


class ContestDraftCodeAPI(APIView):
    @login_required
    def get(self, request):

        if not request.GET.get("problem_id"):
            return self.error("Invalid Parameter")
        if not request.GET.get("language"):
            return self.error("Invalid Parameter")

        problem_id = request.GET.get("problem_id")
        language = request.GET.get("language")
        contest = self.contest
        drafts = DraftCode.objects.filter(user=request.user)
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id=contest.id, visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            draft = drafts.get(problem=problem, language=language)
            result = DraftCodeSafeSerializer(draft).data
            return self.success(result)

    @validate_serializer(UpdateDraftCodeSerializer)
    @login_required
    def put(self, request):
        data = request.data
        id = data["id"]
        checksum = data["checksum"]
        if not data["code"]:
            return self.success()

        problem_id = data["problem_id"]
        if not data["contest_id"]:
            return self.error("Invalid parameter")
        language = data["language"]
        code = data["code"]
        drafts = DraftCode.objects.filter(user=request.user)
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id=data["contest_id"], visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            try:
                draft = drafts.get(problem=problem, language=language)
            except DraftCode.DoesNotExist:
                return self.success("임시저장이 존재하지 않습니다")
            if draft.id == id and draft.checksum == checksum:
                draft = DraftCode.objects.get(id=id, checksum=checksum)
                draft.code = code
                draft.save()
                return self.success(draft.last_update_time)
            return self.error("Invalid checksum")