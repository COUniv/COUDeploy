from django.conf.urls import url
from ..views.admin import BannerTestAPI,Test

urlpatterns = [
    url(r"^banner_test/?$", BannerTestAPI.as_view(), name="banner_test"),
    url(r"^test/?$", Test.as_view(), name="Test"),
]
