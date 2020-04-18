from django.urls import path

from .views import PostListView, PostListUserView, PostDetailsView
from .views import PostCreateView, PostUpdateView, PostDeleteView
from .views import post_share

urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('posts/<str:author>/', PostListUserView.as_view(), name='posts_list_owner'),
    path('post/<str:slug>/', PostDetailsView.as_view(), name='post_detail'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('post/<str:slug>/update/', PostUpdateView.as_view(), name='update_post'),
    path('post/<str:slug>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('post/<str:slug>/share/', post_share, name='share_post'),
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='posts_list_by_tag'),

]
