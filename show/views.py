import os
from show.form import *
from show.models import UserFiles
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.conf import settings
# Create your views here.
STATICFILES_DIRS = settings.STATICFILES_DIRS


def index(request):
    pcount = scount = count = 0
    res = UserFiles.objects.raw(
        "select 1 as id,sum(upload_count) as sum,count(*) as count from show_userfiles group by user_id")
    for i in res:
        pcount += 1
        scount += i.count
        count += i.sum
    info = []
    info_pool = UserFiles.objects.all()[:10]
    for i in info_pool:
        info.append({'name': i.user.username,
                     'pname': i.upload_name, 'time': i.last_upload_time})
        context = {
            'title': 'Test', 
            'count': count, 
            'pcount': pcount, 
            'scount': scount, 
            'info': info
        }
    return render(request, 'index.html', context)


def register_view(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)

        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # profile = UserProfile.objects.create(user=new_user)
            return HttpResponseRedirect('/auth/login', {'regstatus': '注册成功'})
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

    return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required(login_url='/auth/login')
def upload_view(request):
    context = {}
    def handle_upload_files(file, path):
        allow_files = ['zip', 'html', 'js', 'css', 'htm', 'img', 'png', 'jpg']
        if str(file).split('.')[-1] not in allow_files:
            return False

        try:
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + '/' + str(file), 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)
        
            return True
        except Exception:
            return False

    if request.method == 'POST':
        upname = request.POST['uploadname']

        path = os.path.join(
            STATICFILES_DIRS[0], 'show', 'share', request.user.username, upname)

        if handle_upload_files(request.FILES['uploadfile'], path):
            try:
                uf = UserFiles.objects.get(
                    user=request.user, upload_name=upname)
                uf.upload_count += 1
                uf.save()
            except Exception:
                UserFiles(user=request.user, upload_name=upname,
                          upload_files='/' + request.user.username + '/' + upname).save()
            context = {
                'form': UploadForm(), 
                'status': False, 
                'message': '上传成功'
            }
        else:
           context = {
                'form': UploadForm(), 
                'status': False, 
                'message': '上传失败,此文件不在上传范围之内'
           } 
    else:
        context = {'form': UploadForm(), 'status': True}

    return render(request, 'upload.html', context)


@login_required(login_url='auth/login')
def project_view(request):
    info = []
    pj_pool = UserFiles.objects.filter(user=request.user)
    for i in pj_pool:
        info.append({'name':i.upload_name,'time': i.last_upload_time,'url':i.upload_files})

    return render(request, 'project.html', {'info':info})


def share_view(request, name=None, pname=None):
    context = {
        'title': pname + '  --预览',
        'name': name,
        'pname' : pname
    }
    return render(request, 'share.html', context)