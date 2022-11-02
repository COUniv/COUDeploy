from django.conf.urls import url
from ..views.admin import UsingBannerListAPI

urlpatterns = [
  url(r"^usingBanner_list/?$", UsingBannerListAPI.as_view(), name="usingBanner_list")
]
