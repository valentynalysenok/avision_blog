from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from posts.models import Post


def blog(request):
    return render(request, 'base.html')


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'posts.html'


def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'post_details.html', {
        'post': post
    })
