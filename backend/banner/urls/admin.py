from django.conf.urls import url
from ..views.admin import InputBannerAPI,Test,BannerActiveAPI,UsingBannerListAPI,DeleteBannerAPI,BannerListAPI

urlpatterns = [
    url(r"^input_banner/?$", InputBannerAPI.as_view(), name="input_banner"),
    url(r"^test/?$", Test.as_view(), name="Test"),
    ###
    url(r"^banner_active/?$", BannerActiveAPI.as_view(), name="banner_active"),
    url(r"^usingBanner_list/?$", UsingBannerListAPI.as_view(), name="usingBanner_list"),
    url(r"^delete_banner/?$", DeleteBannerAPI.as_view(), name="delete_banner"),
    url(r"^banner_list/?$", BannerListAPI.as_view(), name="banner_list"),
]
