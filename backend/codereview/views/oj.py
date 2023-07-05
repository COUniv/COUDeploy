from datetime import timezone
from ..models import CodeReview, Code, Review, User, CodeReviewNotificationType, CodeReviewNotification
from utils.api import APIView, validate_serializer
from ..serializers import Test_serializers, CodeReviewListSerializer, CodeReviewCreateSerializer, CodeReviewSerializer, CodeReviewModifySerializer, ReviewListSerializer, CodeSerializer, CodeReviewCommentCreateSerializer, CodeReviewCommentModifySerializer, CodeReviewNotificationListSerializer
from account.decorators import login_required
from django.db.models import Q
from django.shortcuts import render


def code_split(code:str) -> list:
    result = code.split('\n')
    return result

class CodeReviewListAPI(APIView):
    """
    게시글 목록 출력 함수
    """
    def get(self, request):
        myself = request.GET.get("myself") # 자기 자신의 게시글만 확인하기 위한 데이터
        sort = request.GET.get("sort") # 게시글 정렬 데이터
        search = request.GET.get("search") # 검색 데이터
        searchtype = request.GET.get("searchtype") # 검색 카테고리
        language = request.GET.get("language") # 검색 프로그래밍 언어
        articles = CodeReview.objects.all() # 전체 게시글

        # 자기 자신의 게시글 / 전체 게시글 분류 시
        if (myself and myself == "1"): # 1 - 자기 자신의 게시글만
            articles = articles.filter(username=request.user.username)

        # 게시글 정렬 시
        if (sort == "1"): # 좋아요 순 정렬인 경우
            articles = articles.order_by('-like_count', '-create_time')
        elif (sort == "2"): # 댓글 순 정렬인 경우
            articles = articles.order_by('-comment_count', '-create_time')

        # 게시글 검색 시
        if search:
            if (searchtype == "0"): # 전체 검색
                articles = articles.filter(Q (title__contains=search) | Q (content__contains=search) | Q (username__contains=search)).distinct()
            elif (searchtype == "1"): # 제목에서 검색
                articles = articles.filter(title__contains=search)
            elif (searchtype == "2"): # 내용에서 검색
                articles = articles.filter(content__contains=search)
            elif (searchtype == "3"): # 작성자명에서 검색
                articles = articles.filter(username__contains=search)

        # 질문 게시판의 경우 원하는 언어의 게시글만 출력
        if language:
            articles = articles.filter(problemtype=language)

        data = self.paginate_data(request, articles) # 페이징
        data["results"] = CodeReviewListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)

class CodeReviewCreateAPI(APIView):
    """
    코드 리뷰 게시글 생성 함수
    """
    @login_required
    @validate_serializer(CodeReviewCreateSerializer)
    def post(self, request): # 디버깅 편의로 GET, 추후 POST로 변경해야 함
        title = request.POST.get("title")
        content = request.POST.get("content")
        username = request.user.username
        code_text = request.POST.get("code")
        if(title is None or content is None or username is None or code_text is None):
            return self.error('need some fields')

        # if CodeReview.objects.exists(): # 게시글이 존재하는 경우
        #     latest_id = CodeReview.objects.order_by('-id')[0].id + 1 # 생성 게시글 ID = 현재 존재하는 가장 높은 ID + 1
        # else: # 아무 게시글도 없는 경우
        #     latest_id = 1 # 생성 게시글 ID = 1
        
        code_objects = Code.objects.create()
        code_objects.origin = code_text
        code_objects.code = code_split(code_text)
        code_objects.save()
        
        CodeReview.objects.create(
            writer = request.user,
            username = username,
            title = title,
            content = content,
            code = code_objects
        )
        
        return self.success()
    
class CodeReviewAPI(APIView):
    """
    코드 리뷰 게시글 details 출력 함수
    """
    def get(self, request):
        article_id = request.GET.get("id") # 파라미터로 전송된 ID값을 통해 게시글 출력
        
        if article_id:
            try:
                article = CodeReview.objects.get(id=article_id) # 해당 ID를 가진 게시글 가져옴
            except:
                return self.error("none data")
            article_data = CodeReviewSerializer(article).data
            # 현재 접속한 유저가 해당 게시글의 작성자 여부
            article_data["is_writer"] = (request.user.username == article.username)
            article_data["code"] = article.code.code
            try: # 해당 ID를 가진 게시글에 달린 댓글 데이터
                comments = Review.objects.filter(target=article_id) # 댓글을 가져옴
                article_data["comments"] = ReviewListSerializer(comments, many=True).data
            except Review.DoesNotExist: # 해당 ID를 가진 댓글이 하나도 없는 경우
               article_data["comments"] = []
               
            # return self.success(ReviewListSerializer(comments, many=True).data)
            return self.success(article_data) # username, title, content, create_time, is_writer, comments 데이터 전송
            
        else:
            return self.error("게시글이 존재하지 않습니다")

class CodeReviewDeleteAPI(APIView):
    """
    코드 리뷰 게시글 삭제 함수
    """
    def post(self, request):
        article_id = request.POST.get("id") #article_id

        if article_id:
            article = CodeReview.objects.get(id=article_id) # 전송된 ID를 통해 게시글을 가져옴
            if request.user.username == article.username: # 해당 게시글 작성자와 현재 접속한 작성자가 같은 경우
                comments = Review.objects.filter(id=article_id) # 해당 게시글의 작성된 댓글
                article.code.delete()
                comments.delete() # 댓글 삭제
                article.delete() # 게시글 삭제
                return self.success()
            else: # 게시글 작성자가 아닌 경우
                return self.error("권한이 없습니다")
        else:
            return self.error("게시글이 존재하지 않습니다")
        
class CodeReviewModifyAPI(APIView):
    """
    코드 리뷰 게시글 수정 함수
    """
    @login_required
    @validate_serializer(CodeReviewModifySerializer)
    def post(self, request):
        title = request.POST.get("title")
        content = request.POST.get("content")
        code = request.POST.get("code")
        codereview_id = request.POST.get("id") # 수정과 달리 이미 존재하는 게시글의 ID를 전송 받음
        
        if codereview_id:
            try:
                codereview = CodeReview.objects.get(id=codereview_id) # 전송받은 ID를 가진 게시글을 수정함 / 신규 생성 X
            except:
                return self.error("have a no id")
            codereview.title = title
            codereview.content = content
            codereview.code = code
            codereview.save()
            return self.success()
        else:
            return self.error("게시글이 존재하지 않습니다")
        
class CodeReviewCommentCreateAPI(APIView):
    """
    댓글 작성 함수
    """
    @login_required
    @validate_serializer(CodeReviewCommentCreateSerializer)
    def post(self, request): # 디버깅 편의로 GET, 추후 POST로 변경해야 함
        data = request.data
        content = data["content"] # 작성할 댓글 내용
        articleid = data["articleid"] # 댓글을 작성할 게시글 ID
        line = int(data["line"])
        
        try:
            article = CodeReview.objects.get(id=articleid)
            user = User.objects.get(username=request.user.username)
        except:
            return self.error()
        article.comment_count += 1 # 댓글을 작성할 게시글의 댓글 수 1 증가
        avatar = user.userprofile.avatar
        temp = Review.objects.create(writer=request.user,
                                    username=request.user.username,
                                    target=article,
                                    content=content,
                                    avatar=avatar,)
        if line:
            temp.line_num = line
            temp.save()
            
        # url = "/codereview_article/" + str(articleid)
        # short_content = "[" + article.title + "]글에 댓글이 달렸습니다."
        # if article.username != request.user.username:
        #     CodeReviewNotification.objects.create(target_username=article.username,
        #                         action_username=request.user.username,
        #                         notificationtype=CodeReviewNotificationType.COMMENT,
        #                         content=short_content,
        #                         comment_content = content,
        #                         url=url)
            
        article.save() # 저장
        return self.success()

        
class CodeReviewCommentDeleteAPI(APIView):
    """
    댓글 삭제 함수
    이상함 고쳐야함
    """
    @login_required
    def get(self, request):
        comment_id = request.GET.get("id") # 삭제할 댓글의 ID

        try:
            comment = Review.objects.get(id=comment_id) # 전송된 ID를 통해 댓글을 가져옴
            
            if comment.writer!=request.user:
                return self.error()
            comment.target.comment_count -= 1 # 게시글의 댓글 수 1 감소
            comment.target.save() # 저장
            comment.delete() # 댓글 삭제
            return self.success()
        except:
            return self.error()

class CodeReviewCommentModifyAPI(APIView):
    """
    댓글 수정 함수
    """
    @login_required
    @validate_serializer(CodeReviewCommentModifySerializer)
    def post(self, request):
        data = request.data
        id = data["id"] # 수정할 댓글의 ID
        content = data["content"] # 수정할 댓글의 내용
        if id:
            comment = Review.objects.get(id=id)
            comment.content = content # 댓글 내용 수정
            comment.save() # 저장
            return self.success()
        else:
            return self.error("해당 댓글이 존재하지 않습니다")
        
class CodeReviewCommentArticleListAPI(APIView):
    def get(self, request):
        username = request.user.username
        
        comments = Review.objects.filter(username = username)

        comment_ids  = []

        for comment in comments:
            comment_ids.append(comment.id)

        articles = CodeReview.objects.filter(id__in = comment_ids)
        data = self.paginate_data(request, articles) # 페이징
        data["results"] = CodeReviewListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)

class GetCode(APIView):
    def get(self, rq):
        code_id = rq.GET.get('id', None)
        if(code_id is None):
            return self.error("err")
        code = Code.objects.get(id=code_id)
        result = CodeSerializer(code)
        return self.success(result.data)
        
class Test(APIView):
    @login_required
    def get(self, request):
        return render(request, 'createriview.html')

class DeleteTest(APIView):
    @login_required
    def get(self, request):
        return render(request, 'deletetest.html')

class CreateComment(APIView):
    @login_required
    def get(self, request):
        return render(request, 'createcomment.html')
        
class Create_review_Test(APIView):
    @login_required
    def get(self, request):
        user = request.user
        c = request.GET.get("code","WTF")

        code_objects = Code.objects.create(code = c)
        result = CodeReview.objects.create(
            writer=user,
            username=user.username,
            title="따흐흑",
            content="어흑",
            code=code_objects,
            )
        
        return self.success("gogo")
    
class Demo(APIView):
    def get(self, request):
        return self.success("ddahuhuk")