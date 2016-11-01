from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, User
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from image_host_app.models import Post, Comment, Profile




class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("post_list_view")


class ProfileListView(ListView):
    model = Profile


class PostListView(ListView):
    model = Post
    paginate_by = 3

class PostCreateView(CreateView):
    model = Post
    fields = ('image', 'title', 'description', 'nsfw')
    success_url = reverse_lazy("profile_list_view")

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post


class PostUpdateView(UpdateView):
    model = Post
    fields = ('image', 'title', 'description', 'nsfw')

    def get_success_url(self, **kwargs):
        return reverse('post_detail_view', args=[int(self.kwargs['pk'])])

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class CommentCreateView(CreateView):
    model = Comment
    fields = ('text', )

    def get_success_url(self, **kwargs):
        return reverse('post_detail_view', args=[int(self.kwargs['pk'])])

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.post = Post.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('text', )

    def get_success_url(self, **kwargs):
        post_id = Comment.objects.get(id=self.kwargs["pk"]).post.id
        return reverse('post_detail_view', args=[post_id])

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
