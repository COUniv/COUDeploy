from django.conf.urls import url
from ..views.oj import Test,Create_review_Test,Demo

urlpatterns = [
    url(r"^codereview_test/?$", Test.as_view(), name="codereview_test"),
    url(r"^codereview_create_test/?$", Create_review_Test.as_view()),
    url(r"^codereview_Demo/?$", Demo.as_view()),
]
