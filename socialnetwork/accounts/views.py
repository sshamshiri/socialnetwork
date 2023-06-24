from django.shortcuts import render , redirect
from django.views import View
from .forms import UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

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
            