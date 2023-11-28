from django.shortcuts import render
from django.views import View
from posts.models import Post
from .forms import PostSearchForm

# Create your views here.


class HomeView(View):
    form_class = PostSearchForm

    def get(self, request):
        posts = Post.objects.all()
        if request.GET.get('search'):
            posts = posts.filter(body__contains=request.GET['search'])
        # posts = Post.objects.order_by('created')
        return render(request, "home/index.html", {'posts': posts, 'form':self.form_class})


