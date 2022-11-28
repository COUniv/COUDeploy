from django.conf.urls import url

from ..views.admin import UserAdminAPI, GenerateUserAPI, AllManagedUserList, ManagedUserListAPI

urlpatterns = [
    url(r"^user/?$", UserAdminAPI.as_view(), name="user_admin_api"),
    url(r"^generate_user/?$", GenerateUserAPI.as_view(), name="generate_user_api"),
    url(r"^all_managed_user_list/?$", AllManagedUserList.as_view(), name="all_managed_user_list_api"),
    url(r"^managed_user_list/?$", ManagedUserListAPI.as_view(), name="managed_user_list_api"),
]
