from django.shortcuts import render
from backend.account.decorators import login_required
from utils.api import APIView
from models import Image

class ImageList(APIView):
    def get(self, request):
        return self.success()
    def post(self, request):
        return self.success()

class ImageUpload(APIView):
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

class ImageDelete(APIView):
    def get(self, request):
        return self.success()