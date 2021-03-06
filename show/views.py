import os
import time
import re
from show.form import *
from show.models import UserFiles,UserUp
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.conf import settings
# Create your views here.
STATICFILES_DIRS = settings.STATICFILES_DIRS


def index(request):
    pcount = scount = count = 0
    res = UserFiles.objects.raw(
        "select 1 as id,sum(submit_count) as sum,count(*) as count from show_userfiles group by user_id")
    for i in res:
        pcount += 1
        scount += i.count
        count += i.sum
    
    info = []
    info_pool = UserFiles.objects.filter(is_ective=0)[:10]
    
    up_pool = []
    if request.user.is_authenticated:    
        up_pool = [i.project_id.id for i in UserUp.objects.filter(up_user=request.user)]

    for i in info_pool:
        t_info = i.info()
        t_info['upflag'] = i.id in up_pool
        info.append(t_info)

    context = {
        'title': '人机交互项目展示中心', 
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
        allow_files = ['zip', 'rar', 'html', 'js', 'css', 'htm', 'img', 'png', 'jpg']
        if str(file).split('.')[-1] not in allow_files:
            return False

        try:
            old_path = os.getcwd()
            if not os.path.exists(path):
                os.makedirs(path)
            with open(path + '/' + str(file), 'wb+') as f:
                for chunk in file.chunks():
                    f.write(chunk)

            # begin unzip
            if str(file).split('.')[-1] == allow_files[0]:
                os.chdir(path)
                import zipfile
                with zipfile.ZipFile(str(file),'r') as f:
                    for i in f.namelist():
                        new_name = ''
                        try:
                            new_name = i.encode('cp437').decode('gbk')
                        except:
                            new_name = i.encode('utf-8').decode('utf-8')
                        f.extract(i)
                        os.rename(i,new_name)
            # end unzip
            return True
        except Exception as e:
            print(e)
            os.chdir(old_path)
            return False

    if request.method == 'POST':
        upname = request.POST['uploadname']

        path = os.path.join(
            STATICFILES_DIRS[0], 'show', 'share', str(request.user.id), upname)

        if handle_upload_files(request.FILES['uploadfile'], path):
            try:
                uf = UserFiles.objects.get(
                    user=request.user, project_name=upname, is_ective=0)
                uf.submit_count += 1
                uf.save()
            except Exception:
                UserFiles(user=request.user, project_name=upname,
                        file_path='/' + str(request.user.id)   + '/' + upname).save()
            context = {
                'form': UploadForm(), 
                'status': False, 
                'message': '上传成功'
            }
        else:
           context = {
                'form': UploadForm(), 
                'status': False, 
                'message': '上传失败,此文件不在上传范围之内或是文件错误，请联系管理员'
           } 
    else:
        context = {'form': UploadForm(), 'status': True}

    return render(request, 'upload.html', context)


@login_required(login_url='/auth/login')
def project_view(request):
    info = []
    nullflag = False
    pj_pool = UserFiles.objects.filter(user=request.user,is_ective=0)
    for i in pj_pool:
        info.append({'id':i.id, 
                     'name':i.project_name, 
                     'time': i.last_submit_time,
                     'url':i.file_path})
    if len(info) == 0:
        nullflag = True
    context = {
        'info': info, 
        'nullflag': nullflag
    }
    return render(request, 'project.html', context)


def share_view(request, name=None, pname=None):
    order_by_l = ["-last_submit_time", "-up_count"]
    if name == None:
        info = []
        up_pool = []
        order_by = int(request.GET.get('type', 0))
        info_pool = UserFiles.objects.filter(is_ective=0).order_by(order_by_l[order_by])
        if request.user.is_authenticated:    
            up_pool = [i.project_id.id for i in UserUp.objects.filter(up_user=request.user)]

        for i in info_pool:
            t_info = i.info()
            t_info['upflag'] = i.id in up_pool
            info.append(t_info)
        context = {
            'info':info,
        }
        return render(request, 'sall.html', context)
    else:
        path = os.path.join(
            STATICFILES_DIRS[0], 'show', 'share', name, pname)
        if os.path.exists(os.path.join(path, 'index.html')):
            context = {
                'title': pname + '  --预览',
                'name': name,
                'pname' : pname,
                'html': 'index.html'
            }
        else:
            for i in os.listdir(path):
                if str(i).endswith('.html'):
                    break
            if not str(i).endswith('.html'):
                return render(request,'404.html')
            context = {
                'title': pname + '  --预览',
                'name': name,
                'pname' : pname,
                'html': i
            }
        return render(request, 'share.html', context)


@login_required(login_url='/auth/login')
def delete_view(request, pid=None):
    pid = int(request.GET.get('pid',0))
    try:
        uf = UserFiles.objects.get(id=pid)
        if request.user == uf.user or request.user.is_superuser:
            uf.is_ective = 1
            uf.save()
            file_path =  uf.file_path.split('/')
            path = os.path.join(STATICFILES_DIRS[0],'show', 'share',file_path[1], file_path[2])
            import shutil
            shutil.rmtree(path)
            
            return JsonResponse({'status': 0})
        else:
            return JsonResponse({'status': -2})
    except Exception as e:
        print (str(e))
        return JsonResponse({'status': -1})

    return JsonResponse({'status': 1})


@login_required(login_url='/auth/login')
def edit_view(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        #保证唯一id不变
        save_flag  = request.POST['username'] == request.user.username
        
        if save_flag and user_form.is_valid():
            user_form.save()
            context = {
                'user_form': user_form,
                'editflag': False,
                'message': '修改成功'
            }
        else:
            context = {
                'user_form': user_form,
                'editflag': False,
                'message': '失败'
            }
    else:
        context = {
            'user_form': UserEditForm(instance=request.user),
            'editflag': True
        }
    return render(request,'auth/edit.html', context)


@login_required(login_url='/auth/login')
def up_view(request):
    """
    TODO
    """
    pid = request.GET.get('pid',0)
    result = {}

    try:
        project = UserFiles.objects.get(id=pid)
    except Exception as e:
        raise e
        result = {'status': -1}
        return JsonResponse(result)
    try:
        uu = UserUp.objects.get(project_id=project, up_user=request.user)
        uu.delete()
        # down / 取消点赞
        project.up_count -= 1 
        result = {'status': 1, 'upcount': project.up_count}
    except Exception:
        UserUp(project_id=project, up_user=request.user).save()
        # up
        project.up_count += 1
        result = {'status': 0,'upcount': project.up_count}
    project.save(auto_now=False)
 
    return JsonResponse(result)


def about_view(request):
    return render(request, 'about.html')


def test_tmp_view(request):
    pattern = re.compile("[A-Z]+")
    res = []
    if request.method == 'POST':
        body = request.POST['answer']
        for i in eval(body)['resInfo']['testQuesList']:
            res.append({'quesIndex': i['quesIndex'], 
                        'quesContent': i['quesContent'][:10],
                        'quesAnswerOption': pattern.findall(i['quesAnswer'])})
        print (res)

    has = len(res) is 0

    return render(request, 'tmp.html', context={'answer': res, 'has': has})