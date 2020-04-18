from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, TemplateView, DetailView

from .forms import PostForm, EmailPostForm
from .models import Post
from .utils import send_email


class BlogView(TemplateView):
    template_name = 'base.html'


class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    context_object_name = 'posts'
    template_name = 'posts.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        """Pagination for posts list view"""
        context = super(PostListView, self).get_context_data(**kwargs)
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
        return context


class PostListUserView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'posts_owner.html'
    paginate_by = 3

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user, status='published')


class PostDetailsView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post_details.html'


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
            # name = form.cleaned_data.get('name')
            # email_from = form.cleaned_data.get('email_from')
            # email_to = form.cleaned_data.get('email_to')
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
