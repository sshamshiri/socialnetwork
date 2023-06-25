from django.shortcuts import render , redirect
from django.views import View
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import PostUpdateForm
from django.utils.text import slugify


class HomeView(View):
    def get(self,request):
        posts = Post.objects.all()
        return render(request, 'home/index.html',{'posts':posts})
    
class PostDetailView(View):
    def get(self,request,post_id,post_slug):
        post = Post.objects.get(pk=post_id,slug=post_slug)
        return render(request, 'home/detail.html',{'post':post})
    
class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id :
            post.delete()
            messages.success(request,'Post deleted successfully','success')
        else:
            messages.error(request,"You can't delete this post",'danger')
        return redirect('home:index')

class PostUpdateView(LoginRequiredMixin,View):
    form_class = PostUpdateForm

    def setup(self , request , *args , **kwargs):
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])
        return super().setup(request,*args , **kwargs)
    
    def dispatch(self , request , *args , **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            messages.success(request, "You can't update this post", 'danger')
            return redirect('home:index')
        return super().dispatch(request , *args , **kwargs)
    
    def get(self , request , *args , **kwargs):
        post = self.post_instance
        form = self.form_class(instance=post)
        return render (request,'home/update.html',{'form':form})