from django.contrib import admin
import os
from django.shortcuts import render
from utils.api import APIView, validate_serializer
from account.decorators import login_required, verify_required
from ..serializers import BannerListSerializer, UsingBannerListSerializer, ImageUploadForm, EditEnableBannerSerializer
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
        if image.size > 2 * 1920 * 800:    #->비율 재조정 필요!
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
        newBanner.url = f"{settings.BANNER_URI_PREFIX}/{name}"
        newBanner.save()
        return self.success("성공")
    
class Test(APIView):
    def get(self,request):
        return render(request, 'uploadimg.html')

#배너 활성화 및 비활성화 컨트롤
class BannerActiveAPI(APIView):
    def get(self, request):
        #query?
        data = request.GET.getlist('checks',None)
        if len(data) == 0:
            return self.success("null values")
        
        for tuple in Using_banner.objects.all():
            t = tuple.banner
            t.isUse = False
            t.save()
            tuple.delete()
        num = 1
        for i in data:
            a = Banner.objects.get(id=i)
            a.isUse=True
            a.save()
            Using_banner.objects.create(banner = a,
                                        priority = num,
                                        url = a.url)
            num +=1
        return self.success("성공")

    @validate_serializer(EditEnableBannerSerializer)
    def put(self, request):
        data = request.data
        if len(data) == 0:
            return self.error("null values")
        banner_id = data["id"]
        enable = data["enable"]
        # disable banner
        if enable == False or enable == 0 or enable == "0":
            single_banner = Banner.objects.get(id=banner_id)
            single_banner.isUse = False
            single_banner.save()
            using_banner = Using_banner.objects.filter(banner__id=banner_id)
            using_banner.delete()

            reorder_banner = Using_banner.objects.all().order_by("priority")
            num = 1
            for ban in reorder_banner:
                ban.priority = num
                ban.save()
                num += 1
            return self.success("비활성화 성공")
        #enable banner
        else:
            num = 1
            enable_banner = Banner.objects.get(id=banner_id)
            enable_banner.isUse = True
            enable_banner.save()
            Using_banner.objects.create(banner = enable_banner,
                                        priority = num,
                                        url = enable_banner.url)
            num += 1
            reorder_banner = Using_banner.objects.all().order_by("priority")
            for ban in reorder_banner:
                ban.priority = num
                ban.save()
                num += 1
            return self.success("활성화 성공")


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
    