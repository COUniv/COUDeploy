from django.conf.urls import url

from ..views.oj import (DraftCodeAPI, ContestDraftCodeAPI)

urlpatterns = [
    url(r"^draft_code/?$", DraftCodeAPI.as_view(), name="draft_code"),
    url(r"^contest/draft_code/?$", ContestDraftCodeAPI.as_view(), name="email_authentication")
]
