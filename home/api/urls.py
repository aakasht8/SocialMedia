from django.urls import path, include

from core.views import (SignUp, Login, Logout, SendFriendRequest, ListFriendRequest, RespondFriendRequest,
                        SearchFriends, ListFriends)

urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('send_request/', SendFriendRequest.as_view()),
    path('list_requests/', ListFriendRequest.as_view()),
    path('respond_request/<req_id>/<action>', RespondFriendRequest.as_view()),
    path('search', SearchFriends.as_view()),
    path('list_friends/', ListFriends.as_view()),

]
