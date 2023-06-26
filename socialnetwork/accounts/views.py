from typing import Any
from django.http.request import HttpRequest
from django.http.response import HttpResponseBase
from django.shortcuts import render , redirect , get_object_or_404
from django.views import View
from .forms import UserRegistrationForm , UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


# Create your views here.
class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get (self,request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})
    
    def post (self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'] , cd['email'] , cd['password1'])
            messages.success(request,'You registerd successfully', 'success')
            return redirect('home:index')
        return render(request , self.template_name , {'form':form})
    
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('home:index')
        return super().dispatch(request, *args, **kwargs)

    def get (self,request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})
    
    def post (self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login (request,user)
                messages.success(request, "you logged in successfully",'success')
                return redirect('home:index')
            messages.error(request, "username or password is wrong",'warning')
        return render(request, self.template_name , {'form':form})

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'You Logged out successfully!','success') 
        return redirect('home:index')
    
class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = get_object_or_404(User,pk=user_id)
        posts = Post.objects.filter(user=user)
        return render(request, 'accounts/profile.html',{'user':user ,'posts':posts})
    
class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    success_url = reverse_lazy ('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complate')

class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'