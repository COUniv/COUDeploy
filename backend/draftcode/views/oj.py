from datetime import timezone
from ..models import DraftCode, Problem, Contest
from utils.api import APIView, validate_serializer
from ..serializers import UpdateDraftCodeSerializer, DraftCodeSafeSerializer, CreateDraftCodeSerializer, DraftLastUpdatedSerializer
from account.decorators import login_required
from django.db.models import Q
from hashlib import sha3_256

class DraftCodeAPI(APIView):

    @validate_serializer(CreateDraftCodeSerializer)
    @login_required
    def post(self, request):
        data = request.data
        if not data.get("contest_id"):
            try:
                problem = Problem.objects.get(_id=data["problem_id"], contest_id__isnull=True, visible=True)
            except Problem.DoesNotExist:
                return self.error("존재하지 않은 문제입니다")
            draft = DraftCode.objects.create(user=request.user, problem=problem, language=data["language"])
        else:
            try:
                contest = Contest.objects.get(id=data["contest_id"], visible=True)
            except Contest.DoesNotExist:
                return self.error("Contest does not exist")
            try:
                problem = Problem.objects.get(_id=data["problem_id"], contest_id=data["contest_id"], visible=True)
            except Problem.DoesNotExist:
                return self.error("존재하지 않은 문제입니다")
            draft = DraftCode.objects.create(user=request.user, problem=problem, contest=contest, language=data["language"])
        draft.save()
        return self.success("make q")

    @login_required
    def get(self, request):
        # contest 는 별도 api로 반환
        if not request.GET.get("problem_id"):
            return self.success("Invalid Parameter")
        if not request.GET.get("language"):
            return self.success("Invalid Parameter")

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
                #쿼리 악용을 방지하기 위한 hashing 값
                msg = 'nonedraftcode' + request.user.username
                h = sha3_256()
                h.update(msg.encode('utf-8'))
                return self.success(h.hexdigest())
            result = DraftCodeSafeSerializer(draft).data
            return self.success(result)
        return self.success("None saved code")

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
                return self.success(DraftLastUpdatedSerializer(draft).data)
            return self.error("Invalid checksum")
        return self.success("successed save code")


class ContestDraftCodeAPI(APIView):
    @login_required
    def get(self, request):
        # 요청 중 나가는 경우를 생각하여 success로 담음
        if not request.GET.get("problem_id"):
            return self.success("Invalid Parameter")
        if not request.GET.get("contest_id"):
            return self.success("Invalid Parameter")
        if not request.GET.get("language"):
            return self.success("Invalid Parameter")

        problem_id = request.GET.get("problem_id")
        contest_id = request.GET.get("contest_id")
        language = request.GET.get("language")
        try:
            contest = Contest.objects.get(id=contest_id, visible=True)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        drafts = DraftCode.objects.filter(user=request.user)
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id=contest_id, visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            try:
                draft = drafts.get(problem=problem, contest=contest, language=language)
            except DraftCode.DoesNotExist:
                #쿼리 악용을 방지하기 위한 hashing 값
                msg = 'nonedraftcode' + request.user.username
                h = sha3_256()
                h.update(msg.encode('utf-8'))
                return self.success(h.hexdigest())
            result = DraftCodeSafeSerializer(draft).data
            return self.success(result)
        return self.success("None saved code")

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
        contest_id = data["contest_id"]
        language = data["language"]
        code = data["code"]
        drafts = DraftCode.objects.filter(user=request.user)
        try:
            contest = Contest.objects.get(id=contest_id, visible=True)
        except Contest.DoesNotExist:
            return self.error("Contest does not exist")
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id=data["contest_id"], visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            try:
                draft = drafts.get(problem=problem, contest=contest, language=language)
            except DraftCode.DoesNotExist:
                return self.success("임시저장이 존재하지 않습니다")
            if draft.id == id and draft.checksum == checksum:
                draft = DraftCode.objects.get(id=id, checksum=checksum)
                draft.code = code
                draft.save()
                return self.success(DraftLastUpdatedSerializer(draft).data)
            return self.error("Invalid checksum")
        return self.success("successed save code")