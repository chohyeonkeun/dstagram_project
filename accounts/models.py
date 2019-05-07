from django.db import models

# Create your models here.
# 중간 모델 작성
from django.contrib.auth import get_user_model
User = get_user_model()

class Follow(models.Model):
    # 2개 필드 - ForeignKey
    # A가 B를 팔로우 하고 있다. 라고 가정
    # on_delete : 연관된 객체가 삭제된다면 어떻게 할 것이냐?
    # related_name : 참조 객체의 입장에서 필드명, 속성값
    me = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    you = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')

    def __str__(self):
        return self.me.username+" follow "+self.you.username

'''
example)
Follow model
id  me you
1   1   3    # 1번이 3번을 follow
2   1   2    # 1번이 2번을 follow
3   2   1    # 2번이 1번을 follow
4   3   1    # 3번이 1번을 follow
--> me에서 특정 번호 count하면 following 숫자 나옴
--> you에서 특정 번호 count하면 follower 숫자 나옴
'''