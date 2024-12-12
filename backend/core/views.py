from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from .models import Channel,User
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    ChangePassowrdSerializer,
    CreateChannelSerializer, 
    RegisterSerializer,
    PublicChannelSerializer,
    UserSerializer)

# Create your views here.



class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "User created successfully and logged in.",
        })

class UserProfileUpdateApi(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully!",
                "user": serializer.data,
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChannelDetailView(generics.GenericAPIView):
    serializer_class = CreateChannelSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Retrieve the user's channel
        try:
            channel = Channel.objects.get(owner=request.user)
            serializer = CreateChannelSerializer(channel)
            return Response(serializer.data)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args,  **kwargs):
        #verify if the user is truly the one tryna make a channel
        if f'{request.user.pk}'==request.data['owner']:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            channel = serializer.save()
            return Response({
                "message": "Channel Created Successfully."
            })
        else :
            return Response({
            "message":"tryna be sneaky ey?"
        })
    def put(self, request, *args, **kwargs):
        try:
            instance = Channel.objects.get(pk=request.user.pk)
        except Channel.DoesNotExist:
            return Response({
                "message": "Channel not found."
            })

        if f'{request.user.pk}' == str(instance.owner.pk):
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            channel = serializer.save()
            return Response({
                "message": "Channel updated.",
            })
        else:
            return Response({
                "message": "Trying to be sneaky, ey?"
            },)
    
    def patch(self, request, *args, **kwargs):
        try:
            instance = Channel.objects.get(pk=request.user.pk)
        except Channel.DoesNotExist:
            return Response({
                "message": "Channel not found."
            })

        if f'{request.user.pk}' == str(instance.owner.pk):
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            channel = serializer.save()
            return Response({
                "message": "Channel partially updated.",
            })
        else:
            return Response({
                "message": "Trying to be sneaky, ey?"
            })

class SubscribeChannelView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        channel = get_object_or_404(Channel, pk=pk)

        if channel.subscribers.filter(id=request.user.id).exists():
            # Unsubscribe if already subscribed
            channel.subscribers.remove(request.user)
            return Response({'message': f'Unsubscribed from {channel.name}.'}, status=status.HTTP_200_OK)
        else:
            # Subscribe
            channel.subscribers.add(request.user)
            return Response({'message': f'Subscribed to {channel.name}.'}, status=status.HTTP_200_OK)

class PublicChannelListView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = PublicChannelSerializer

class PublicChannelDetailView(generics.RetrieveAPIView):
    queryset = Channel.objects.all()
    serializer_class = PublicChannelSerializer
    lookup_field = 'pk'



class ChangePasswordAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePassowrdSerializer
    def put(self, request, *args, **kwargs):
        try:
            user = request.user
        except user.DoesNotExist:
            #better be safe than sorry
            return Response({
                "message": "user not found."
            })

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "password updated.",
        })
    
class ChangePasswordAPI(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePassowrdSerializer
    def put(self, request, *args, **kwargs):
        try:
            user = request.user
        except user.DoesNotExist:
            #better be safe than sorry
            return Response({
                "message": "user not found."
            })

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "password updated.",
        })
    

