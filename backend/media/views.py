from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Movie, Video, VideoRating, ReportVideo, ReportRating
from core.models import Channel
from .serializers import  VideoFileSerializer, VideoRatingSerializer, ReportVideoSerializer, VideoEditSerializer, ReportRatingSerializer
# Create your views here.

class VideoUploadViewSet(ModelViewSet):
    queryset = Video.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]  # Public view, restricted edit
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['genre']  # Filter by genre
    search_fields = ['title', 'description']  # Search by title/description
    ordering_fields = ['views', 'date']  # Order by views (popularity) or date
    ordering = ['-date']  # Default ordering: newest first
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return VideoEditSerializer
        return VideoFileSerializer

    def perform_update(self, serializer):
        video = self.get_object()
        # Ensure the logged-in user owns the channel
        if video.channel.owner != self.request.user:
            raise PermissionDenied("You do not have permission to edit this video.")
        serializer.save()

    def perform_create(self, serializer):
        # Get the logged-in user's channel
        user = self.request.user
        
        try:
            # Ensure the user has a channel, or you can create one if needed
            channel = Channel.objects.get(owner=user)
        except Channel.DoesNotExist:
            raise PermissionDenied("You must have a channel to upload a video.")
        
        # Now, set the channel to the video data dynamically (without passing it in the request)
        serializer.save(channel=channel)

class VideoRatingViewSet(viewsets.ModelViewSet):
    queryset = VideoRating.objects.all()
    serializer_class = VideoRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(commentor=self.request.user)

    def perform_update(self, serializer):
        video_rating = self.get_object()
        if video_rating.commentor != self.request.user:
            raise PermissionDenied("You can only edit your own ratings.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.commentor != self.request.user:
            raise PermissionDenied("You can only delete your own ratings.")
        instance.delete()

class ReportVideoViewSet(viewsets.ModelViewSet):
    queryset = ReportVideo.objects.all()
    serializer_class = ReportVideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(video_reporter=self.request.user)

class ReportRatingViewSet(viewsets.ModelViewSet):
    queryset = ReportRating.objects.all()
    serializer_class = ReportRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rating_reporter=self.request.user)
