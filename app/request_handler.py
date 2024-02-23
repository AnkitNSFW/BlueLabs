from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET
from utility.assests_links import asset_urls
from utility.app_db import UserLogin, user_exist, update_user_last_login_timestamp, set_otp, fetch_user_name, check_otp_and_make_user, check_login_status
from utility.email_functions.email_notification import send_signup_notifiction
from utility.email_functions.email_templates import TEMP_EMAIL_LIST


@require_GET
def login_get(request):
    user_data = check_login_status(request)
    if not user_data:
        context={}
        context['asset_urls'] = asset_urls
        return render(request, 'app/login.html', context=context)
    else:
        return redirect('/home')

@require_POST
def login_post(request):
    context={}
    context['asset_urls'] = asset_urls
    user_id = request.POST['id']
    user_password = request.POST['password']
    msg, jwt_token = UserLogin(user_id=user_id, user_password=user_password)
    if jwt_token:
        update_user_last_login_timestamp(user_id=user_id)
        request.session['auth_token'] = jwt_token
        return redirect('/home')
    else:
        context['msg']=msg
        context['user_id'] = request.POST['id']
        return render(request, 'app/login.html' ,context=context)



@require_GET
def sign_up_get(request):    
    user_data = check_login_status(request)
    if user_data:
        return redirect('/home')
    else:
        return render(request, 'app/signup/signup.html', context={'asset_urls': asset_urls})

@require_POST
def sign_up_post(request):
    msg, context = '', {}

    user_id = request.POST['id']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    password1 = request.POST['password1']
    password2 = request.POST['password2']

    context['user_id'] = user_id
    context['first_name'] = first_name
    context['last_name'] = last_name

    if user_exist(user_id):
        msg = "The Email Already Exist, Please Login"
        context['password1'] = password1
        context['password2'] = password2
    elif user_id.split('@')[1] in TEMP_EMAIL_LIST:
        msg = "Temperory email are not allowed, Please use a proper email."
    elif password1 != password2:
        msg = "Password don't match"
    else:
        request.session['user_id'] = user_id
        set_otp(user_id=user_id, first_name=first_name, last_name=last_name, password=password1)
        return redirect('/validate_otp')

    context['msg']=msg
    return render(request, 'app/signup/signup.html', context=context)



@require_GET
def validate_otp_get(request):
    context = {}
    context['asset_urls'] = asset_urls
    user_data = check_login_status(request)
    if user_data:
        context['first_name']=user_data['first_name']
        return redirect('/home')
    else:
        if request.session.get('user_id', None):
            return render(request, 'app/signup/validate_otp.html', context=context)
        else:
            return redirect('/')

@require_POST
def validate_otp_post(request):
    context = {}
    context['asset_urls'] = asset_urls
    user_id = request.session['user_id']
    otp = request.POST['otp']
    otp_status, otp_msg = check_otp_and_make_user(user_id=user_id, otp=otp)
    if otp_status:
        msg, jwt_token = UserLogin(user_id=user_id, user_password=otp_msg)
        if jwt_token:
            update_user_last_login_timestamp(user_id=user_id)
            request.session['auth_token'] = jwt_token
            return redirect('/home')
        
    context['msg'] = otp_msg
    return render(request, 'app/signup/validate_otp.html', context=context)