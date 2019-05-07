from django.shortcuts import render
import requests
# Create your views here.
# 유저 목록이 출력되는 뷰
# + 기능 Follow라는 기능
# 중간 테이블을 직접 생성 - 모델

# 나(유저 모델)
# 나를 팔로우한 사람 필드 생성
# 내가 팔로우한 사람 필드 생성
# 유저 모델을 커스터마이징 -> 1. 커스터마이징 하는 방법을 배운다.(커스터마이징 할 수가 없다면?)
# 확장하는 방법에 따라서
# 1) 새로운 유저 모델 만드는 방법 --> 기존 유저 데이터를 유지할 수가 없다.(수동으로 데이터 옮겨야 함)
# 2) 기존 모델을 확장하는 방법 --> DB 다운 타임 발생(DB 잠시 멈춰야 함) alter table  할 때 table lock 걸림


# 사진 모델
# 사진을 좋아요 누른 사람 필드 생성
# 사진을 저장한 사람 필드 생성


'''
1. 유저 목록 혹은 유저 프로필에서 팔로우 버튼
1-1.  전체 유저 목록을 출력해주는 뷰 - User 모델에 대한 ListView

2. 팔로우 정보를 저장하는 뷰
'''
from django.contrib.auth.models import User

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.http import HttpResponseForbidden
from .models import Follow
from .forms import SignUpForm

class UserList(ListView):
    model = User
    template_name = 'accounts/user_list.html'

def signup(request):
    # Class Based View -> dispatch -> get, post
    if request.method == "POST":
        # Todo : 입력받은 내용을 이용해서 회원 객체 생성
        # 입력받은 내용 확인하기
        # 모델 폼을 이용해서 코드를 간결하게 바꾼다.
        signup_form = SignUpForm(request.POST)
        # form validation
        if signup_form.is_valid():
            # 1. 저장하고 인스턴스 생성
            user_instance = signup_form.save(commit=False)
            # 2. 패스워드 암호화 -> 저장
            # 폼이 가지고 있는 cleaned_data란? : 유효한 문자만 남긴 상태로 처리 과정을 거친 데이터
            user_instance.set_password(signup_form.cleaned_data['password'])
            user_instance.save()
            return render(request, 'accounts/signup_complete.html', {'username': user_instance.username})
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # email = request.POST.get('email')

        # 회원 객체 생성하기
        # user = User()
        # user.username = username
        # user.set_password(password)
        # user.first_name = first_name
        # user.last_name = last_name
        # user.email = email
        # user.save()


    else:
        # Todo : form 객체를 만들어서 전달
        signup_form = SignUpForm()
        # context_values = {'form':signup_form}
        # 템플릿 연동 순
        # 1. 템플릿 불러오기
        # 2. 템플릿 렌더링하기
        # 3. HTTP Response하기
    return render(request, 'accounts/signup.html', {'form':signup_form})

# class UserFollow(View):
#     def get(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             r서eturn HttpResponseRedirect('/accounts/signin')
#         else:
#             user = request.user
#             follow = Follow.objects.filter(me=user)
#             pass

class UserFollowerList(ListView):
    model = User
    template_name = 'accounts/follower_list.html'

class UserFollowingList(ListView):
    model = User
    template_name = 'accounts/following_list.html'

class UserFollower(View):
    def get(self, request, *args, **kwargs):
        pass


class UserFollowing(View):
    def get(self, request, *args, **kwargs):
        pass


