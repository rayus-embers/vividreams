from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VideoUploadViewSet,VideoRatingViewSet, ReportVideoViewSet, ReportRatingViewSet

router = DefaultRouter()
#router.register('movies', MovieViewSet)
router.register(r'videos', VideoUploadViewSet, basename='video')
router.register('video-ratings', VideoRatingViewSet)
router.register('report-videos', ReportVideoViewSet)
router.register('report-ratings', ReportRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Include all viewsets
]
