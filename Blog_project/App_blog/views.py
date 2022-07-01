from dataclasses import fields
from pyexpat import model
from re import template
from django.shortcuts import render,HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView,TemplateView

from Blog_project.settings import CACHE_TTL

from .models import Blog,Comment,Liked
from .forms import CommentForm
import uuid

#redis
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
# Create your views here.

CACHE_TTL=getattr(settings,'CACHE_TTL',DEFAULT_TIMEOUT)



class CreateBlog(LoginRequiredMixin,CreateView):
    model=Blog
    template_name='App_blog/create_blog.html'
    fields=('blog_title','blog_content','blog_image',)


    def form_valid(self, form):
        blog_obj=form.save(commit=False)
        blog_obj.author=self.request.user
        title=blog_obj.blog_title
        blog_obj.slug=title.replace(" ","-") + "-" + str(uuid.uuid4())
        blog_obj.save()
        return HttpResponseRedirect(reverse('index'))


class MyBLog(LoginRequiredMixin,TemplateView):
    template_name='App_blog/my_blogs.html'

class EditBlog(LoginRequiredMixin,UpdateView):
    model=Blog
    fields=('blog_title','blog_content','blog_image')
    template_name='App_blog/edit_blog.html'

    def get_success_url(self,**kwargs):
        return reverse_lazy('App_blog:blog_details',kwargs={'slug':self.object.slug})

class BlogList(ListView):
    context_object_name='blogs'
    model=Blog
    template_name='App_blog/blog_list.html'

@login_required
def blog_details(request,slug):
    
    blog=Blog.objects.get(slug=slug)
    comment_form=CommentForm()
    already_liked=Liked.objects.filter(blog=blog,user=request.user)
    if already_liked:
        liked=True
    else:
        liked=False
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.user= request.user
            comment.blog=blog
            comment.save()
            return HttpResponseRedirect(reverse("App_blog:blog_details",kwargs={'slug':slug}))

    return render(request,'App_blog/blog_details.html',context={'blog':blog,'comment_form':comment_form,'liked':liked,})


@login_required
def like_post(request,pk):
    blog=Blog.objects.get(pk=pk)
    user=request.user
    already_liked=Liked.objects.filter(blog=blog,user=user)
    if not already_liked:
        liked_post=Liked(blog=blog,user=user)
        liked_post.save()
    return HttpResponseRedirect(reverse("App_blog:blog_details",kwargs={'slug':blog.slug}))


@login_required
def unliked_post(request,pk):
    blog=Blog.objects.get(pk=pk)
    user=request.user
    already_like=Liked.objects.filter(blog=blog,user=user)
    already_like.delete()
    return HttpResponseRedirect(reverse("App_blog:blog_details",kwargs={'slug':blog.slug}))
