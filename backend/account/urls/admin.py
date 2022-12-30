from django.conf.urls import url

from ..views.admin import UserAdminAPI, GenerateUserAPI, AllManagedUserList, ManagedUserListAPI, SendEmailForUsersAPI

urlpatterns = [
    url(r"^send_mail_for_users/?$", SendEmailForUsersAPI.as_view(), name="send_mail_for_users_api"),
    url(r"^user/?$", UserAdminAPI.as_view(), name="user_admin_api"),
    url(r"^generate_user/?$", GenerateUserAPI.as_view(), name="generate_user_api"),
    url(r"^all_managed_user_list/?$", AllManagedUserList.as_view(), name="all_managed_user_list_api"),
    url(r"^managed_user_list/?$", ManagedUserListAPI.as_view(), name="managed_user_list_api"),
]
