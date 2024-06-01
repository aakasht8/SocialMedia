import datetime

from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from rest_framework import status, authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication

from core.models import FriendRequest
from core.serializers import UserSerializer, LoginSerializer, FriendRequestSerializer, GetFriendRequestSerializer, \
    SearchUserSerializer


# Create your views here.


class SignUp(APIView):
    def post(self, request):
        # for user sign up
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Log user in
            user_login = auth.authenticate(username=user.username, password=request.data['password'])
            if user_login:
                # auth.login(request, user_login)
                return Response({'message': 'User created in successfully'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'User created, but failed to log in'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):

    def post(self, request):
        # for user login
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            # auth.login(request, user)
            return Response({'message': 'User logged in successfully', 'token': str(token)}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # for user logout
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)


class SendFriendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        sender = request.user
        receiver_id = request.data.get('receiver_id')
        # Check if the receiver exists
        try:
            receiver = User.objects.get(pk=receiver_id)
        except User.DoesNotExist:
            return Response({'message': 'Receiver does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Check if a friend request already exists
        if FriendRequest.objects.filter(Q(sender=sender, receiver=receiver) |
                                        Q(sender=receiver, receiver=sender)).exists():
            return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the sender has sent more than 3 friend requests within the last minute
        one_minute_ago = timezone.now() - timezone.timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(sender=sender, timestamp__gte=one_minute_ago).count()

        if recent_requests_count >= 3:
            return Response({'message': 'You have sent more than 3 friend requests'
                                        ' within the last minute. Please try again later.'},
                            status=status.HTTP_429_TOO_MANY_REQUESTS)

        # Create and save the friend request with status 'PENDING'
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListFriendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        curr_user = request.user
        friend_requests = FriendRequest.objects.filter(receiver=curr_user.id, status='PENDING')
        serializer = GetFriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RespondFriendRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, req_id, action):
        try:
            friend_request = FriendRequest.objects.get(id=req_id)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=status.HTTP_400_BAD_REQUEST)
        if action == '1':
            # Accept the friend request
            message = 'Friend request accepted'
            friend_request.status = 'ACCEPTED'
        elif action == '0':
            # Reject the friend request
            message = 'Friend request rejected'
            friend_request.status = 'REJECTED'
        else:
            return Response({'error': 'Invalid action performed'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request.save()
        return Response({'message': message}, status=status.HTTP_200_OK)


class SearchFriends(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        search_keyword = request.GET.get('search', '')

        if not search_keyword:
            return Response({'error': 'Search keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

        # for exact match on email
        users = User.objects.filter(email=search_keyword)

        if not users.exists():
            # for partial match on name
            users = User.objects.filter(username__icontains=search_keyword)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = SearchUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)


class ListFriends(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        friends = []
        curr_user = request.user
        friends_queryset = FriendRequest.objects.filter(Q(receiver_id=curr_user.id, status='ACCEPTED')
                                               | Q(sender_id=curr_user.id, status='ACCEPTED'))
        for friend_request in friends_queryset:
            if friend_request.sender == curr_user:
                friends.append(friend_request.receiver)
            else:
                friends.append(friend_request.sender)
        serializer = SearchUserSerializer(friends, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
