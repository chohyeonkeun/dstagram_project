from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from .views import *

app_name = "accounts"

urlpatterns = [
    path('user/followerlist/', UserFollowerList.as_view(), name='follower_list'),
    path('user/followinglist/', UserFollowingList.as_view(), name='following_list'),
    path('user/list/', UserList.as_view(), name='user_list'),
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('signout/', LogoutView.as_view(template_name='accounts/signout.html'), name='signout'),
    path('signup/', signup, name='signup'),
]


