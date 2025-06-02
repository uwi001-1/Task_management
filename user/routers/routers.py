from rest_framework.routers import DefaultRouter
from ..viewsets.user_viewsets import userViewsets

router = DefaultRouter()

router.register('user', userViewsets, basename="userViewsets") 