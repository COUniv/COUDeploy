from ..models import CodeReview, Code, Review
from utils.api import APIView, validate_serializer
from ..serializers import Test_serializers
from account.decorators import login_required

class Test(APIView):
    @login_required
    def get(self, request):
        data = CodeReview.objects.all()
        
        result = Test_serializers(data, many=True)
        //result['data']['code_text'] = Code.objects.get(id=2).code
        return self.success(result.data)
        
        
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