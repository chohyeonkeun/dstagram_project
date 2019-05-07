from django.db import models

# Create your models here.
# 기본 모델

'''

작성자 : author
본문글 : text
사진 : image
작성일 : created
수정일 : updated

+ tag, like
-- comment

'''
# from django.contrib.auth.models import User
# reverse --> url pattern 이름을 가지고 주소를 만들어주는 함수
from django.urls import reverse
# User 모델을 확장 가능
# settings.AUTH_USER_MODEL
from django.contrib.auth import get_user_model

class Photo(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='photos')   # ForeignKey(User, 삭제 시 동작, 연관 이름)
    # models.ForeignKey(get_user_model(), )  --> 확장할 거라면 요렇게 쓰는 걸 추천
    # CASCADE --> 연속해서 지운다. 탈퇴하면 사진도 싹 지운다.
    # PROTECT --> 사진 다 안지우면 너 탈퇴 안됨 - 탈퇴 프로세스에 사진을 우선 삭제하고 탈퇴시킨다.
    # 특정값으로 셋팅 -
    # reletaed_name 으로 연관 데이터를 얻을 수 없다면 쿼리를 별도로 실행해야 한다.
    # 내 프로필 페이지 - 내가 올린 사진만 뜬다.
    # pillow --> python에서 image를 올리기 위한 라이브러리리
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to='timeline_photo/%Y/%m.%d')   # %Y/%m/%d --> 자동으로 연/월/일 생성해준다.
    # upload_to 는 함수를 사용해서 폴더를 동적으로 설정할 수 있다.
    created = models.DateTimeField(auto_now_add=True)   # 처음 생성할 때만 지정
    updated = models.DateTimeField(auto_now=True)   # 처음 생성할때, 수정할때마다 지정

    like = models.ManyToManyField(get_user_model(), related_name='like_post')
    saved = models.ManyToManyField(get_user_model(), related_name='saved_post')

    class Meta:
        ordering = ['-created']

    def get_absolute_url(self):
        # detail/<int:pk>/ 여기에 들어갈 값을 self.id로 던져준다.
        return reverse('photo:detail', args=[self.id])