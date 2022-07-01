from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login,logout,authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import UserSignUp,ChangeProfileForm,AddProfilePicForm

# Create your views here.

def signup_form(request):
    form=UserSignUp()
    registered=False
    if request.method=='POST':
        form=UserSignUp(data=request.POST)
        if form.is_valid():
            form.save()
            registered=True

    dict={'form':form,'registered':registered}
    return render(request,'App_login/signup.html',context=dict)


def login_form(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)

        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
    
    return render(request,'App_login/login.html',context={'form':form})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_profile(request):
    return render(request,'App_login/profile.html',context={})


@login_required
def change_user_profile(request):
    current_user=request.user
    form=ChangeProfileForm(instance=current_user)
    if request.method=='POST':
        form=ChangeProfileForm(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            form=ChangeProfileForm(instance=current_user)

    return render(request,'App_login/change_profile.html',context={'form':form})

@login_required
def change_password(request):
    change=False
    current_user=request.user
    form=PasswordChangeForm(current_user)
    if request.method=='POST':
        form=PasswordChangeForm(current_user,request.POST)
        if form.is_valid():
            form.save()
            change=True
    return render(request,'App_login/pass_change.html',context={'form':form,'change':change})

@login_required
def add_profile_pic(request):
    form=AddProfilePicForm()
    if request.method=='POST':
        form=AddProfilePicForm(request.POST,request.FILES)
        if form.is_valid():
            user_obj=form.save(commit=False)
            user_obj.user=request.user
            user_obj.save()
            return HttpResponseRedirect(reverse('App_login:profile'))
    return render(request,'App_login/Add_profile_pic.html',context={'form':form})


@login_required
def change_picture(request):
    form=AddProfilePicForm(instance=request.user.user_profile)
    if request.method=='POST':
        form=AddProfilePicForm(request.POST,request.FILES,instance=request.user.user_profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_login:profile'))
    return render(request,'App_login/Add_profile_pic.html',context={'form':form})