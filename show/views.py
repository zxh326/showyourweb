from .form import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect  

# Create your views here.

def index(request):
    return render(request,'index.html')


def register_view(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # profile = UserProfile.objects.create(user=new_user)
            return HttpResponseRedirect('/auth/login',{'regstatus':'注册成功'})
    else:
        user_form = RegisterForm()
    return render(request, 'auth/reg.html', {'form': user_form})


def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 获取表单用户名和密码
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 进行用户验证
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                context = {
                    'message': '登陆成功',
                    'status': True
                }
                # return render(request, 'index.html', context)
                return HttpResponseRedirect(request.POST.get('next', '/') or '/')
            else:
                form = LoginForm()
                context = {
                    'message': '密码或账号错误',
                    'status': False,
                    'form': form,
                }
                return render(request, 'auth/login.html', context)
    else:
        context = {'form': LoginForm(), 'status': True}

    return render(request,'auth/login.html',context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')