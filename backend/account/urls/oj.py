from django.conf.urls import url

from ..views.oj import (ApplyResetPasswordAPI, ResetPasswordAPI,
                        UserChangePasswordAPI, UserRegisterAPI, UserChangeEmailAPI,
                        UserLoginAPI, UserLogoutAPI, UsernameOrEmailCheck,
                        AvatarUploadAPI, TwoFactorAuthAPI, UserProfileAPI,
                        UserRankAPI, CheckTFARequiredAPI, SessionManagementAPI,
                        ProfileProblemDisplayIDRefreshAPI, OpenAPIAppkeyAPI, SSOAPI, UserDeleteAPI,
                        GrassAPI, getFindUserIDAPI, UserRatingChartAPI, MyRatingChartAPI, UserRatingRankAPI)

from ..views.oj import (ApplyVerifyEmailAPI, VerifyEmailAPI, LastActivityAPI)
from ..views.admin import (ForceUpdateAllUserRatingAPI)
from utils.captcha.views import CaptchaAPIView

urlpatterns = [
    url(r"force_update_all_user_rating/?$", ForceUpdateAllUserRatingAPI.as_view(), name="force_update_all_user_rating"),
    url(r"get_user_rating_rank/?$", UserRatingRankAPI.as_view(), name="get_user_rating_rank"),
    url(r"get_user_rating_chart/?$", UserRatingChartAPI.as_view(), name="get_user_rating_chart"),
    url(r"get_my_rating_chart/?$", MyRatingChartAPI.as_view(), name="get_mt_rating_chart"),
    url(r"get_find_username/?$", getFindUserIDAPI.as_view(), name="get_find_username"),
    url(r"^get_inactive_time/?$", LastActivityAPI.as_view(), name="get_inactive_time_api"),
    url(r"^apply_verify_email/?$", ApplyVerifyEmailAPI.as_view(), name="apply_verify_email_api"),
    url(r"^verify_email/?$", VerifyEmailAPI.as_view(), name="verify_email_api"),
    url(r"^login/?$", UserLoginAPI.as_view(), name="user_login_api"),
    url(r"^logout/?$", UserLogoutAPI.as_view(), name="user_logout_api"),
    url(r"^register/?$", UserRegisterAPI.as_view(), name="user_register_api"),
    url(r"^change_password/?$", UserChangePasswordAPI.as_view(), name="user_change_password_api"),
    url(r"^change_email/?$", UserChangeEmailAPI.as_view(), name="user_change_email_api"),
    url(r"^apply_reset_password/?$", ApplyResetPasswordAPI.as_view(), name="apply_reset_password_api"),
    url(r"^reset_password/?$", ResetPasswordAPI.as_view(), name="reset_password_api"),
    url(r"^captcha/?$", CaptchaAPIView.as_view(), name="show_captcha"),
    url(r"^check_username_or_email", UsernameOrEmailCheck.as_view(), name="check_username_or_email"),
    url(r"^get_grass_data/?$", GrassAPI.as_view(), name="get_grass"),
    url(r"^profile/?$", UserProfileAPI.as_view(), name="user_profile_api"),
    url(r"^profile/fresh_display_id", ProfileProblemDisplayIDRefreshAPI.as_view(), name="display_id_fresh"),
    url(r"^upload_avatar/?$", AvatarUploadAPI.as_view(), name="avatar_upload_api"),
    url(r"^tfa_required/?$", CheckTFARequiredAPI.as_view(), name="tfa_required_check"),
    url(r"^two_factor_auth/?$", TwoFactorAuthAPI.as_view(), name="two_factor_auth_api"),
    url(r"^user_rank/?$", UserRankAPI.as_view(), name="user_rank_api"),
    url(r"^sessions/?$", SessionManagementAPI.as_view(), name="session_management_api"),
    url(r"^open_api_appkey/?$", OpenAPIAppkeyAPI.as_view(), name="open_api_appkey_api"),
    url(r"^sso?$", SSOAPI.as_view(), name="sso_api"),
    url(r"^delete_account/?$", UserDeleteAPI.as_view(), name="delete_account"),
]
