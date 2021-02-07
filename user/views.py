from django.shortcuts import render,redirect,get_object_or_404,HttpResponse, Http404, HttpResponseRedirect, reverse
from .forms import RegisterForm, LoginForm, UserUpdateForm
from .models import User
from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission
from urllib.parse import urlencode
from django.conf import settings
# Create your views here.

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    context = {
            "form" : form
        }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        name = form.cleaned_data.get("name")
        surname = form.cleaned_data.get("surname")
        picture = form.cleaned_data.get("picture")
        gender = form.cleaned_data.get('gender')

        group = Group.objects.get(name='default')

        registeredUser = User(username = username,name = name, gender=gender,picture=picture ,surname = surname , email = email)
        registeredUser.set_password(password)
        registeredUser.group = group
        registeredUser.save()
        login(request, registeredUser)
                
        return redirect('view_post')
    return render(request,"user/register.html",context)
        
def loginUser(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(username = username)
        if len(user) != 1:
            messages.info(request,"User does not exist.")
            return render(request,'user/login.html',{'form':form})
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                messages.info(request,"Password doesn't match.")
                return HttpResponse("<b<Password doesn't match")
        messages.success(request,"Giriş Başarılı")
        login(request,user)
        return redirect('view_post')
        #return redirect(reverse('view', kwargs={'username':request.user.username}))
    
    return render(request,'user/login.html',{'form':form})

def logoutUser(request):
    logout(request)
    messages.success(request,"You are logout succesfully")
    return redirect('login')


@login_required(login_url = "index")
def change_user(request,username):
    if (not request.user.is_authenticated) and (not request.user.username == username):
        raise Http404

    user = get_object_or_404(User, username=username)
    form = UserUpdateForm(data=request.POST or None, files = request.FILES or None, instance=user)

    if form.is_valid():
        updatedUser = form.save(commit=False)
        for data in form.changed_data:
            updatedUser.data = form.cleaned_data.get(data)
        
        updatedUser.set_password(form.cleaned_data.get('password'))
        updatedUser.save()
        login(request, updatedUser)
        
        return redirect(reverse('user-view', kwargs={'username':request.user.username}))
    return render(request, 'back_end/user/edit.html',{'form':form})

@login_required(login_url = "user:login")
def view_user(request,username):
    if request.user.is_authenticated:
        if request.user.username == username:

            return render(request,'back_end/user/view.html')
        
    return HttpResponse('<b>Sayfayı Görüntülemek İçin Yetkiniz Yok</b>')




