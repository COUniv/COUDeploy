from django.contrib import admin
import os
from django.shortcuts import render
from utils.api import APIView
from account.decorators import login_required, verify_required
from ..serializers import BannerListSerializer, UsingBannerListSerializer, ImageUploadForm
from ..models import Banner,Using_banner
from django.conf import settings
from utils.shortcuts import rand_str


class InputBannerAPI(APIView):
    request_parsers = ()

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        
        if form.is_valid():
            image = form.cleaned_data["image"]
            title = form.cleaned_data["title"]
            url = form.cleaned_data["url"]
        else:
            return self.error("올바른 형식이 아니야!")
        if image.size > 2 * 1024 * 1024:    #->비율 재조정 필요!
            return self.error("이미지의 사이즈가 너무 커!")
        suffix = os.path.splitext(image.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("지원하지 않는 포맷입니다")

        name = rand_str(10) + suffix
        while os.path.exists(os.path.join(settings.BANNER_UPLOAD_DIR, name)):
            name = rand_str(10) + suffix
            
        with open(os.path.join(settings.BANNER_UPLOAD_DIR, name), "wb") as img:
            for chunk in image:
                img.write(chunk)
                
        newBanner = Banner.objects.create()
        newBanner.banner = f"{settings.BANNER_URI_PREFIX}/{name}"
        newBanner.title = title
        newBanner.url = url
        newBanner.save()
        return self.success("성공")
    
class Test(APIView):
    def get(self,request):
        return render(request, 'uploadimg.html')

#배너 활성화 및 비활성화 컨트롤
class BannerActiveAPI(APIView):
    def post(self, request):
        #query?
        data = request.POST.getlist('checks')
        
        for tuple in Using_banner.objects.all():
            tuple.banner.isUse = False
            tuple.delete()
        num = 1
        for i in data:
            a = Banner.objects.get(id=i)
            a.isUse=True
            a.save()
            Using_banner.objects.create(banner = a,
                                        priority = num,
                                        url = "url")
            num +=1
        return self.success()

class BannerListAPI(APIView):
    def get(self,request):
        data = BannerListSerializer(Banner.objects.all(), many=True)
        return self.success(data.data)
    
#메인 페이지 banner 리턴
class UsingBannerListAPI(APIView):
    def get(self,request):
        banner = Using_banner.objects.all().order_by("priority")
        data = UsingBannerListSerializer(banner, many=True)
        
        return self.success(data.data)
    
class DeleteBannerAPI(APIView):
    def get(self, request):
        id = request.data.get("id")
        if not id : return self.error()
        banner = Banner.objects.get(id=id)
        file_path = settings.DATA_DIR + banner.banner
        
        if os.path.exists(file_path):
            os.remove(file_path)
            banner.delete()
        else:
            self.error("존재하지않는 파일")
            
        return self.success("제거 성공!")
    