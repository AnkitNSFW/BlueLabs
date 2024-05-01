from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

import sys
sys.path.append('')
from utility.utility_func import jwt_decode
from notion.widgetUpdateFuncs import config_function_dict, add_function_dict, delete_widget, add_widgets, widget_function_dict
from utility.assests_links import asset_urls
from utility.notion_db import fetch_user_widgets, fetch_widget_congif, widget_owner_check
from utility.app_db import check_login_status

# temp import for widget3 development
from notion.models import NotionWidgets


@require_GET
def home(request):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    
    context={}
    context['asset_urls'] = asset_urls
    context['widgets'] = []
    user_widgets = fetch_user_widgets(user_id=user_data['user_id'])
    for widget in user_widgets:
        context['widgets'].append(
            {"name": widget.name,
            "widget_name": widget.widget_name,
                "widget_id": widget.widget_id,
                "widget_config": widget.widget_config}
        )
    return render(request, 'notion/home.html', context=context)

@require_GET
def configWidget(request, widget_id=None):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    
    if widget_id:
        context = {}
        context['asset_urls'] = asset_urls
        context['widget_id'] = widget_id
        widget_name, widget_congif = fetch_widget_congif(widget_id)
        context['widget_name']=widget_name
        return render(request, f"notion/config/{widget_name}config.html", context=context|widget_congif)
    else:
        return HttpResponse("Please Enter a Valid Widget Config URL")

@require_POST
def addWidget(request):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    widget_name = request.POST['widget_name']
    status = add_widgets(widget_name=widget_name, user_id=user_data['user_id'])
    if status:
        add_function_dict[widget_name](owner=user_data['user_id'], widget_name=widget_name)
        # return redirect('/notion')
        return JsonResponse({'status': True})
    else:
        # return 'Limit Exceded, cannot make more widgets of this kind.'
        return JsonResponse({'status': False})

@require_GET
def deleteWidget(request, widget_id):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    
    if widget_owner_check(widget_id=widget_id, owner=user_data['user_id']):
        delete_widget(widget_id=widget_id, user_id = user_data['user_id'])
    # need to add else condition
    return redirect('/notion')

@require_POST
def updateWidget(request, widget_name, widget_id):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    
    if widget_name and widget_id:
        config_function_dict[widget_name](request=request, owner=user_data['user_id'], widget_name=widget_name, widget_id=widget_id)
        return redirect('/notion')
    else:
        return HttpResponse("The config link is not Valid")

@csrf_exempt
@require_POST
def widgetFunctons(request, widget_id):
    if NotionWidgets.objects.filter(widget_id=widget_id).exists():
        widget = NotionWidgets.objects.get(widget_id=widget_id)
        function_responce = widget_function_dict[widget.widget_name](request, widget)
        return JsonResponse(function_responce)
    else:
        return JsonResponse({'status': False})

@csrf_exempt
@xframe_options_exempt
def widget(request, widget_id=None):
    if widget_id:
        context = {}
        context['asset_urls'] = asset_urls
        context['widget_id'] = widget_id
        widget_name, widget_congif = fetch_widget_congif(widget_id)
        if widget_name:
            return render(request, f"notion/widgets/{widget_name}.html", context=context|widget_congif)
        else:
            return render(request, f"notion/widgets/widget-do-not-exist.html")
    else:
        return HttpResponse("Please Enter a Valid Widget URL")
