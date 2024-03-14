
from django import forms
from django.contrib import admin
from .models import *
# Register your models here.

from ckeditor_uploader.widgets import CKEditorUploadingWidget


def nullfy_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)

nullfy_quantity.short_description = 'Обнулить Посты'

class PostAdminForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'category']
    list_filter = ['author', 'category']
    search_fields = ['author', 'category']
    actions = [nullfy_quantity]
    form = PostAdminForm




admin.site.register(User)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostCategory)