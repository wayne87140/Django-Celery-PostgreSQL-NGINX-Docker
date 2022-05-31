from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from account.utils.update import update_individual_user_info

# Create your views here.
def login(request):
    template = 'account/login.html'
    
    if request.user.is_authenticated:
        return redirect('main:main')
    
    if request.method == 'GET':
        return render(request, template, {'nextURL': request.GET.get('next')})
    
#   POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username or not password:
        messages.error(request, '請填資料')
        return render(request, template)
    
    update_individual_user_info(username)
    user = authenticate(username=username, password=password)
    if not user:
        messages.error(request, '登入失敗')
        return render(request, template)
    
    auth_login(request, user)
    nextURL = request.POST.get('nextURL')
    if nextURL:
        return redirect(nextURL)
    messages.success(request, '登入成功')
    return redirect('main:main')


    
@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, '已登出')
    return redirect('account:login')


