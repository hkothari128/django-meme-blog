from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.views.generic.edit import FormMixin
from django.urls import reverse
from .models import Post
from .forms import CommentForm
from requests import get as url_get
from json import loads as load_json

# posts = [
#     {
#         'author': 'Huzaifa K',
#         'title': 'Blog Post 1',
#         'content': 'First post content',
#         'date_posted': 'August 27,2019',
#     },
#     {
#         'author': 'Husain K',
#         'title': 'Blog Post 2',
#         'content': 'EScond post content',
#         'date_posted': 'August 28,2019',
#     }
# ]


# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        context = super().get_context_data(**kwargs)
        context['posts_commented_on'] = [] if current_user.is_anonymous else list(current_user.comments.values_list('post__id',flat=True))
        dadJokeJson = load_json(url_get('https://icanhazdadjoke.com/slack').content)
        context['dadjoke'] = dadJokeJson['attachments'][0]['text']
        # context['posts_liked'] = [] if current_user.is_anonymous else list(current_user.likes.values_list('post__id',flat=True))
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(FormMixin, DetailView):
    model = Post
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        current_user = self.request.user
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.object
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)

class PostLikeToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
                
        obj = get_object_or_404(Post, pk=kwargs['pk'])
        print(obj)
        
        url_ = obj.get_absolute_url()
        user = self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return url_

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    # success_url = get_success_url()

    def get_success_url(self):
        
        return reverse('blog-home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


def about(request):
    return render(request, 'blog/about.html', {'title': 'about'})
