from django.urls import path

from .views import PostListView, post_details


urlpatterns = [
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/', post_details, name='post_detail'),
]
