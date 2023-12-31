from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Post, Comment, Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostCreatedUpdateForm, CommentCreateForm, CommentReplyForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.


class PostDetailView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'], slug=kwargs['post_slug'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # post = Post.objects.get(pk=post_id, slug=post_slug)
        comments = self.post_instance.post_comments.filter(is_reply=False)
        return render(request, 'posts/detail.html',
                      {'post': self.post_instance, 'comments': comments, 'form': self.form_class,
                       'reply_form': self.form_class_reply})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.post_instance
            new_comment.save()
            messages.success(request, 'sent', 'success')
            return redirect('posts:post_detail', self.post_instance.id, self.post_instance.slug)



class PostDeleteView(LoginRequiredMixin, View):

    def get(self, request, post_id):
        # post = get_object_or_404(Post, pk=post_id)
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'You deleted one post.', 'success')
        else:
            messages.error(request, "You can't delete this post.", "danger")

        return redirect('home:home')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreatedUpdateForm

    def setup(self, request, *args, **kwargs):
        # self.post_instance = get_object_or_404(Post, pk=kwargs['post_id'])
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.error(request, "You can't update other posts.", 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render(request, 'posts/update.html', {'form': form})

    def post(self, request, *args, **kwargs):
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:20])
            new_post.save()
            messages.success(request, "You updated a post.", "success")
            return redirect("posts:post_detail", post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = PostCreatedUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, 'posts/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['title'][:20])
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'Post has been created successfully.', 'success')
            return redirect('posts:post_detail', new_post.id, new_post.slug)


class PostAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    def post(self, request, post_id, comment_id):
        post = get_object_or_404(Post, id=post_id)
        comment = get_object_or_404(Comment, id=comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.post = post
            reply.reply = comment
            reply.is_reply = True
            reply.save()
            messages.success(request, "sent", 'success')
            return redirect("posts:post_detail", post_id, post.slug)

class PostLikeView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        like = Vote.objects.filter(post=post, user=request.user)
        if like.exists():
            messages.error(request, "You liked this post before.", "danger")
        else:
            Vote.objects.create(post=post, user=request.user)
            messages.success(request, 'You liked this post.', 'success')
        return redirect('posts:post_detail', post.id, post.slug)



