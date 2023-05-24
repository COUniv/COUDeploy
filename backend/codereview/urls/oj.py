from django.conf.urls import url
from ..views.oj import (Test, Create_review_Test, Demo, CodeReviewListAPI, CodeReviewCreateAPI, CodeReviewAPI, 
                        CodeReviewDeleteAPI, CodeReviewModifyAPI, GetCode)

urlpatterns = [
    url(r"^codereview_list/?$", CodeReviewListAPI.as_view(), name="codereview_list"),
    url(r"^create_codereview/?$", CodeReviewCreateAPI.as_view(), name="create_codereview"),
    url(r"^codereview/?$", CodeReviewAPI.as_view(), name="codereview"),
    url(r"^delete_codereview/?$", CodeReviewDeleteAPI.as_view(), name="delete_codereview"),
    url(r"^modify_codereview/?$", CodeReviewModifyAPI.as_view(), name="modify_codereview"),
    url(r"^get_code_text/?$", GetCode.as_view(), name="get_code"),
    url(r"^codereview_test/?$", Test.as_view(), name="codereview_test"),
    url(r"^codereview_create_test/?$", Create_review_Test.as_view()),
    url(r"^codereview_Demo/?$", Demo.as_view()),
]
