from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.db.models.functions import Greatest
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView, DetailView
from taggit.models import Tag

from .forms import PostForm, EmailPostForm, CommentForm, SearchForm
from .models import Post, Category
from .utils import send_email


class BlogView(TemplateView):
    template_name = 'base.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    context_object_name = 'posts'
    template_name = 'posts.html'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self, **kwargs):
        posts = Post.objects.filter(status='published')
        try:
            if self.kwargs['tag_slug']:
                tag = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
                posts = Post.objects.filter(tags__in=[tag], status='published')
                return posts
        except KeyError:
            return posts

    def get_context_data(self, **kwargs):
        """With pagination for posts list view"""
        context = super(PostListView, self).get_context_data(**kwargs)

        if self.kwargs.get('category'):
            category = get_object_or_404(Category, title=self.kwargs.get('category'))
            posts = Post.objects.filter(category=category.id, status='published')
        else:
            posts = self.get_queryset()

        page = self.request.GET.get('page')
        paginator = Paginator(posts, self.paginate_by)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context['posts'] = posts
        if self.kwargs.get('tag_slug'):
            context['tag'] = get_object_or_404(Tag, slug=self.kwargs.get('tag_slug'))
        if self.kwargs.get('category'):
            context['category'] = get_object_or_404(Category, title=self.kwargs.get('category'))
        return context


class PostListUserView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts_owner.html'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, status='published')


class PostDetailsView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.model.objects.get(slug=self.kwargs.get('slug'))

        # get list of similar posts
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = self.model.objects.filter(tags__in=post_tags_ids, status='published') \
            .exclude(id=post.id)
        similar_posts_to = similar_posts.annotate(same_tags=Count('tags')) \
                               .order_by('-same_tags', '-publish')[:4]
        similar_posts_from = similar_posts.annotate(same_tags=Count('tags')) \
                                 .order_by('-same_tags', '-publish')[4:]

        context['comments'] = post.comments.filter(active=True)
        context['similar_posts_to'] = similar_posts_to
        context['similar_posts_from'] = similar_posts_from
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        try:
            if request.method == 'POST':
                form = CommentForm(request.POST)
                form.instance.post = self.model.objects.get(slug=self.kwargs.get('slug'))
                form.instance.user = self.request.user
                form.save()
                return redirect('posts:post_detail', slug=self.kwargs.get('slug'))
            return redirect('posts:post_detail', slug=self.kwargs.get('slug'))
        except ValueError:
            return redirect('users:django_registration_register')


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('posts:posts_list')
    success_message = ""

    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.author.is_staff or form.instance.author.is_superuser:
            form.instance.status = 'published'
            self.success_message = "Your post added successfully."
        else:
            self.success_message = "Your post added and waiting for moderation."
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update posts """
        obj = self.get_object()
        if obj.author != self.request.user:
            messages.error(request, 'Restricted access. You are not owner of this post.')
            return redirect(obj)
        return super(PostUpdateView, self).dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts:posts_list')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can delete posts """
        obj = self.get_object()
        if obj.author != self.request.user and not request.user.is_superuser:
            messages.error(request, 'Restricted access. You are not owner of this post.')
            return redirect(obj)
        return super(PostDeleteView, self).dispatch(request, *args, **kwargs)


def post_share(request, slug):
    form = EmailPostForm()
    post = get_object_or_404(Post, slug=slug, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"Avision Blog - {cd.get('name')} recommends you reading {post.title}"
            message = f"Read {post.title} at {post_url} with {cd.get('name')}'s comments:\n " \
                      f"{cd.get('comments')} \n" \
                      f"sender email: {cd.get('email_from')}"
            send_email(subject, message, (cd.get('email_to'),))
            sent = True
    return render(request, 'post_share.html', {
        'post': post,
        'form': form,
        'sent': sent
    })


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                similarity=Greatest(TrigramSimilarity('title', query), TrigramSimilarity('body', query))) \
                .filter(similarity__gt=0.3) \
                .order_by('-similarity')
    return render(request, 'post_search.html', {'form': form,
                                                'query': query,
                                                'results': results})


def post_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.likes.add(request.user)
    post.dislikes.remove(request.user)
    post.save()
    return redirect('posts:post_detail', slug=slug)


def post_dislike(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.dislikes.add(request.user)
    post.likes.remove(request.user)
    post.save()
    return redirect('posts:post_detail', slug=slug)
