from django.conf.urls import url
from ..views.oj import (Test,DeleteTest,CreateComment, Create_review_Test, Demo, CodeReviewListAPI, CodeReviewCreateAPI, CodeReviewAPI, 
                        CodeReviewDeleteAPI, CodeReviewModifyAPI, GetCode, CodeReviewCommentCreateAPI, CodeReviewCommentDeleteAPI, 
                        CodeReviewCommentModifyAPI, CodeReviewCommentArticleListAPI)

urlpatterns = [
    url(r"^codereview_list/?$", CodeReviewListAPI.as_view(), name="codereview_list"),
    url(r"^create_codereview/?$", CodeReviewCreateAPI.as_view(), name="create_codereview"),
    url(r"^codereview/?$", CodeReviewAPI.as_view(), name="codereview"),
    url(r"^delete_codereview/?$", CodeReviewDeleteAPI.as_view(), name="delete_codereview"),
    # url(r"^modify_codereview/?$", CodeReviewModifyAPI.as_view(), name="modify_codereview"),
    url(r"^create_codereview_comment/?$", CodeReviewCommentCreateAPI.as_view(), name="create_codereview_comment"),
    url(r"^delete_codereview_comment/?$", CodeReviewCommentDeleteAPI.as_view(), name="delete_codereview_comment"),
    url(r"^modify_codereview_comment/?$", CodeReviewCommentModifyAPI.as_view(), name="modify_codereview_comment"),
    url(r"^comment_codereview_list/?$", CodeReviewCommentArticleListAPI.as_view(), name="comment_codereview_list"),
    
    url(r"^get_code_text/?$", GetCode.as_view(), name="get_code"),
    
    url(r"^codereview_test/?$", Test.as_view(), name="codereview_test"),
    url(r"^deletecodereview_test/?$", DeleteTest.as_view(), name="deletecodereview_test"),
    url(r"^createcomment_test/?$", CreateComment.as_view(), name="createcomment_test"),
    # url(r"^deletecomment_test/?$", DeleteTest.as_view(), name="deletecomment_test"),
    
    # url(r"^codereview_create_test/?$", Create_review_Test.as_view()),
    url(r"^codereview_Demo/?$", Demo.as_view()),
]
