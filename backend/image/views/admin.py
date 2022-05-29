import os
from django.shortcuts import render
from pip import main
from account.decorators import login_required
from account.serializers import ImageUploadForm
from utils.api import APIView
from ..models import Image
from ..serializers import ImageListSerializer, ImageSerializer

from django.conf import settings

class ImageAPI(APIView):
    def get(self, request):
        image_id = request.GET.get("image_id")
        if image_id:
            image = Image.objects.get(id=image_id)
            return self.success(ImageSerializer(image).data)
        else:
            return self.error("Wrong Image")

class ImageListAPI(APIView):
    def get(self, request):
        images = Image.objects.all()
        data = self.paginate_data(request, images)
        data["results"] = ImageListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)

class ImageUploadAPI(APIView):
    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data["image"]
            name = form.cleaned_data["name"]
            login = form.cleaned_data["login"]
            main = form.cleaned_data["main"]
        else:
            return self.error("Invalid file content")


        if ((main == "true") or (login == "true")):
            if Image.objects.filter(is_main_page = True).count() > 6:
                return self.error("Main page image full")
            if Image.objects.filter(is_login_page = True).count() > 6:
                return self.error("Login page image full")


        if image_file.size > 2 * 1024 * 1024:
            return self.error("Picture is too large")
        
        suffix = os.path.splitext(image_file.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("Unsupported file format")
        
        name = name + suffix
        with open(os.path.join(settings.AVATAR_UPLOAD_DIR, name), "wb") as img: # DIR 변경 필요
            for chunk in image_file:
                img.write(chunk)

        if Image.objects.exists():
            latest_id = Image.objects.order_by('id')[0].id + 1
        else:
            latest_id = 1 

        image = Image.objects.create(id = latest_id,
                                     name = name)
        
        if (login == "true"):
            image.is_login_page = True
            if (main == "true"):
                image.is_main_page = True
            else:
                image.is_main_page = False
        else:
            image.is_login_page = False
            if (main == "true"):
                image.is_main_page = True
            else:
                image.is_main_page = False              
        


        image.save()

        return self.success()

class ImageModifyAPI(APIView):
    def post(self, request):
        data = request.data
        image_id = data["id"]
        main = data["main"]
        login = data["login"]

        if image_id:
            image = Image.objects.get(id=image_id)
            if (login == "true"):
                image.is_login_page = True
                if (main == "true"):
                    image.is_main_page = True
                else:
                    image.is_main_page = False
            else:
                image.is_login_page = False
                if (main == "true"):
                    image.is_main_page = True
                else:
                    image.is_main_page = False
            
            if ((main == "true") or (login == "true")):
                if Image.objects.filter(is_main_page = True).count() > 6:
                    return self.error("Main page image full")
                if Image.objects.filter(is_login_page = True).count() > 6:
                    return self.error("Login page image full")

            image.save()
            return self.success()
        else:
            return self.error("Wrong Image")

class ImageDeleteAPI(APIView):
    def get(self, request):
        image_id = request.GET.get("image_id")
        if image_id:
            image = Image.objects.get(id=image_id)
            image.delete()
            return self.success()
        else:
            return self.error("Wrong Image")

class MainImageListAPI(APIView):
    def get(self, request):
        main_images = Image.objects.filter(is_main_page = True)
        return self.success(ImageListSerializer(main_images, many=True).data)

class LoginImageListAPI(APIView):
    def get(self, request):
        login_images = Image.objects.filter(is_login_page = True)
        return self.success(ImageListSerializer(login_images, many=True).data)

