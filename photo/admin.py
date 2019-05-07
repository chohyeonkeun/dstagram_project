from django.contrib import admin

# Register your models here.

from .models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'image', 'created', 'updated']

    list_filter = ['created', 'updated']

    search_fields = ['created', 'updated', 'text']

    ordering = ['-updated', '-created']

    raw_id_fields = ['author'] # select 박스 방식을 id 입력방식로 바꾸겠다.


admin.site.register(Photo, PhotoAdmin)