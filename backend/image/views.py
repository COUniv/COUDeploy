from django.shortcuts import render
from backend.account.decorators import login_required
from utils.api import APIView
from models import Image
from serializers import ImageListSerializer, ImageSerializer

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
    @login_required
    def get(self, request):
        data = request.data
        path = data["path"]
        login = data["login"]
        main = data["main"]

        if Image.objects.exists():
            latest_id = Image.objects.order_by('id')[0].id + 1
        else:
            latest_id = 1 

        image = Image.objects.create(id = latest_id,
                                     path = path)
        
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
        