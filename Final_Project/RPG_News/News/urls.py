from django.urls import path, include
from django.contrib import admin
from .views import *
urlpatterns = [
    path('news/', NewsList.as_view(), name='post_list'),
    path('author_now/', author_now, name='author_now'),
    path('news/<int:pk>/', NewsDetail.as_view(), name='post'),
    path('news/create/', NewsCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', NewsUpload.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('comment/<int:pk>', CommentDetailView.as_view(), name='comment' ),
    path('create_comment/<int:pk>/', CommentCreateView.as_view(), name='create_comment'),
    path('comment_edit/<int:pk>', CommentUpdateView.as_view, name='comment_update'),
    path('comment_delete/<int:pk>', CommentDeleteView.as_view, name='comment_delete'),
    path('comment_as/<int:comment_id>', comment_accept, name='comment_accept'),
]