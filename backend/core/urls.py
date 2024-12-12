from django.urls import path
from .views import ChangePasswordAPI, PublicChannelListView, PublicChannelDetailView, SubscribeChannelView,RegisterApi, ChannelDetailView

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register user"),
    path('changepass/', ChangePasswordAPI.as_view(), name="change password"),
    path('channel/', ChannelDetailView.as_view(), name='channel-list'),
    path('channels/', PublicChannelListView.as_view(), name='channel-list'),
    path('channels/<int:pk>/', PublicChannelDetailView.as_view(), name='channel-detail'),
    path('channels/<int:pk>/subscribe/', SubscribeChannelView.as_view(), name='channel-subscribe'),
]

