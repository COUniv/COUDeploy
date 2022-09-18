from django.contrib import admin
import os
from django.shortcuts import render
from utils.api import APIView
from account.decorators import login_required, verify_required
from ..serializers import BannerListSerializer,ImageUploadForm
from ..models import Banner
from django.conf import settings
from utils.shortcuts import rand_str


class BannerTestAPI(APIView):
    #@login_required
    #@verify_required
    def post(self, request):
        #요청 -> 폼으로 변환해서 이미지 받기
        form = ImageUploadForm(request.data,request.FILES)
        #request.data? request.POST? request.body?
        
        #파일 유효설 검사
        if form.is_valid():
            banner = form.cleaned_data["image"]
            #title = form.cleaned_data["title"]
        else:
            return self.error("Invalid file content")
        
        #사이즈 체크 
        """if avatar.size > 2 * 1024 * 1024:
            return self.error("Picture is too large")"""
        
        #확장자 검사
        suffix = os.path.splitext(banner.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("Unsupported file format")

        #파일생성
        name = rand_str(10) + suffix
        with open(os.path.join(settings.BANNER_UPLOAD_DIR, name), "wb") as img:
            for chunk in banner:
                img.write(chunk)
            
        #주소 적용
        newBanner = Banner.objects.create()
        newBanner.banner = f"{settings.BANNER_URI_PREFIX}/{name}"
        #newBanner.title = title
        newBanner.save()
        
        return self.success("성공하였습니다")
    
class Test(APIView):
    def get(self,request):
        return render(request, 'uploadimg.html')