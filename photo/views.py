from django.shortcuts import render

# Create your views here.
# CRUDL - 이미지를 띄우는 방법
# 제네릭 뷰
# 쿼리셋 변경하기, context_data 추가하기, 권한 체크
# 함수형 뷰 <-> 클래스형 뷰
from django.shortcuts import redirect

from .models import Photo

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.views.generic.list import ListView

from django.views.generic.detail import DetailView

from django.views.generic.base import View

from django.http import HttpResponseRedirect

from django.http import HttpResponseForbidden

from django.contrib import messages



from urllib.parse import urlparse

# 뷰를 실행하기 전에 특정한 로직을 추가로 실행하고 싶다.
# 로그인 여부, csrf 체크를 수행할 것이냐?
# 믹스인 : 클래스형 뷰
# 데코레이터 : 함수형 뷰 ---- 클래스형 뷰
from django.contrib.auth.mixins import LoginRequiredMixin
# --> 로그인을 했는지 안했는지 확인해주고 로그인 안했으면, 로그인 페이지로 이동시켜줌(경로 설정 필요)

class PhotoList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'


class PhotoCreate(CreateView):
    model = Photo
    fields = ['author', 'image', 'text']
    template_name_suffix = '_create'

    def form_valid(self, form):
        # 입력된 자료가 올바른지 체크
        form.instance.author_id = self.request.user.id  # form.instance.[필드명]_id
        if form.is_valid():
            # 올바르다면,
            # form : 모델 폼
            form.instance.save()
            return redirect('/')
        else:
            # 올바르지 않다면,
            return self.render_to_response({'form':form})  # render 함수 쓰는게 더 좋다.

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['author', 'image', 'text']
    template_name_suffix = '_update'

    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "수정할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


class PhotoDelete(DeleteView):
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    # Life cycle - iOS, Android, Vue, React, Django, Rails
    # 모든 Framework는 라이프 사이클이 존재 --> 어떤 순서로 구동이 되느냐?
    # URLConf -> View -> Model 순으로 동작
    # 라이프 사이클 : 어떤 뷰를 구동할 때 그 안에서 동작하는 순서

    # 사용자가 접속했을 때 get인지 post인지 등을 결정하고 분기하는 부분
    def dispatch(self, request, *args, **kwargs):
        object = self.get_object()
        if object.author != request.user:
            messages.warning(request, "삭제할 권한이 없습니다.")
            return HttpResponseRedirect(object.get_absolute_url())
        else:
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

    # 로직을 수행하고, 템플릿을 랜더링한다.
    # def get(self, request, *args, **kwargs):
    #     object = self.get_object()
    #     if object.author != request.user:
    #         messages.warning(request, "삭제할 권한이 없습니다.")
    #         return HttpResponseRedirect(object.get_absolute_url())
    #         # 삭제 페이지에서 권한이 없다! 라고 띄우는 방법
    #         # 원래 디테일 페이지로 돌아가서 삭제에 실패했습니다! 라고 띄우는 방법
    #     else:
    #         super(PhotoDelete, self).get(request, *args, **kwargs)
    # def post(self, request, *args, **kwargs):
    #     pass
    #
    # def get_object(self, queryset=None):
    #     # 해당 쿼리셋을 이용해서 현재 페이지에 필요한 object를 인스턴스화 한다.
    #     pass
    #
    # def get_queryset(self):
    #     # 어떻게 데이터를 가져올 것이냐?
    #     pass

class PhotoDetail(DetailView):
    model = Photo
    template_name_suffix = '_detail'

class PhotoLike(View):
    def get(self, request, *args, **kwargs):
        # like를 할 정보가 있다면 진행, 없다면 중단
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/signin')
        else:
            #1. 어떤 포스팅?
            # url : www.naver.com/blog/like/?photo_id=1
            # request.GET.get('photo_id')
            # url : www.naver.com/blog/like/1/
            # path('blog/like/<int:photo_id>/'
            # kwargs['photo_id']
            # 2. 누가?
            '''
            id  photo_id  like
            1       1      A
            2       1      B
            3       2      B
            4       2      A
            '''
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.like.all():
                    photo.like.remove(user)
                else:
                    photo.like.add(user)
            referer_url = request.META.get('HTTP_REFERER')
            path = urlparse(referer_url).path
            return HttpResponseRedirect(path)
        # LOGIN_URL = reverse_lazy('accounts:signin')


class PhotoSaved(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        else:
            if 'photo_id' in kwargs:
                photo_id = kwargs['photo_id']
                photo = Photo.objects.get(pk=photo_id)
                user = request.user
                if user in photo.saved.all():
                    photo.saved.remove(user)
                else:
                    photo.saved.add(user)
            return HttpResponseRedirect('/')

'''
saved field
id  photo_id  user
1      1       A   # A가 photo_id 1번을 저장
2      1       B   # B가 photo_id 1번을 저장
3      2       A   # A가 photo_id 2번을 저장
4      3       C   # C가 photo_id 3번을 저장

'''

class PhotoSaveList(ListView):
    model = Photo
    template_name_suffix = '_saved'



class PhotoLikeList(LoginRequiredMixin, ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):  # SQL 에서 SELECT 문과 비슷하다.
        # 로그인한 유저가 좋아요를 클릭한 글을 찾아서 반환
        user = self.request.user
        queryset = user.like_post.all()
        return queryset


class PhotoMylist(ListView):
    model = Photo
    template_name = 'photo/photo_list.html'

    def get_queryset(self):
        user = self.request.user
        queryset = user.photos.all()
        return queryset