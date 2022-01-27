from django.urls import path ,include
from .views import (
    MovieViewSet,
    CommentViewSet,
    VoteViewset
)
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'' , MovieViewSet)
router.register(r'' , CommentViewSet)
router.register(r'' , VoteViewset)


urlpatterns = [
    path('' , include(router.urls)),
]
