from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .models import ForumThread, Post
from .forms import ThreadForm, PostForm

def is_moderator(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

class ThreadListView(ListView):
    model = ForumThread
    template_name = 'forum/thread_list.html'
    context_object_name = 'threads'

class ThreadDetailView(DetailView):
    model = ForumThread
    template_name = 'forum/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['post_form'] = PostForm()
        return ctx

@login_required
def create_post(request, thread_slug):
    thread = get_object_or_404(ForumThread, slug=thread_slug)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.thread = thread
            post.save()
    return redirect('forum:thread_detail', slug=thread.slug)

@user_passes_test(is_moderator)
def create_thread(request):
    if request.method == 'POST':
        form = ThreadForm(request.POST)
        if form.is_valid():
            thread = form.save(commit=False)
            thread.created_by = request.user
            thread.save()
            return redirect('forum:thread_detail', slug=thread.slug)
    else:
        form = ThreadForm()
    return render(request, 'forum/thread_form.html', {'form': form})

@user_passes_test(is_moderator)
def delete_thread(request, slug):
    thread = get_object_or_404(ForumThread, slug=slug)
    if request.method == 'POST':
        thread.delete()
        return redirect('forum:thread_list')
    return render(request, 'forum/thread_confirm_delete.html', {'thread': thread})
