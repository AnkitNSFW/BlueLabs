from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse

import sys
sys.path.append('')
from app.models import UserCred
from notion.models import NotionWidgets, WidgetsTracker
from utility.utility_func import create_uuid, current_DT

widgets_allowed_per_user = {
    'widget1': 3,
    'widget2': 1,
    'widget3': 3
}

def delete_widget(widget_id, user_id):
    parent_id = UserCred.objects.get(user_id=user_id).id
    user_record = WidgetsTracker.objects.get(parent=parent_id)
    if NotionWidgets.objects.filter(widget_id=widget_id).exists():
        widget = NotionWidgets.objects.get(widget_id=widget_id)
        widget_name = widget.widget_name
        widget.delete()
        user_record.widget_count[widget_name] -= 1
        user_record.save()

def add_widget1(owner, widget_name):
    NotionWidgets(
        parent = UserCred.objects.get(user_id=owner),
        widget_id = create_uuid(),

        name = 'BTC-USDT',
        user_id = owner,
        widget_config = {
            'background_color': 'rgb(25,25,25)',
            'currency': 'USDT',
            'hover_on': False,
            'refreshRate': 30,
            'ticker': 'btc'
        },
        widget_name = widget_name,

        created_at = current_DT(),
        modified_at = current_DT()
    ).save()

def add_widget2(owner, widget_name):
    NotionWidgets(
        parent = UserCred.objects.get(user_id=owner),
        widget_id = create_uuid(),

        name = 'Fear & Greed Index',
        user_id = owner,
        widget_config = {
            'background_color': 'rgb(25,25,25)',
            'text_color': 'text-white'
        },
        widget_name = widget_name,

        created_at = current_DT(),
        modified_at = current_DT()
    ).save()

def add_widget3(owner, widget_name):
    NotionWidgets(
        parent = UserCred.objects.get(user_id=owner),
        widget_id = create_uuid(),

        name = 'Counter',
        user_id = owner,
        widget_config = {
            'count': 0,
            'background_color': 'rgb(25,25,25)',
            'text_color': 'text-white'
        },
        widget_name = widget_name,

        created_at = current_DT(),
        modified_at = current_DT()
    ).save()

add_function_dict = {
    'widget1': add_widget1,
    'widget2': add_widget2,
    'widget3': add_widget3
}


# Config Widgets
def config_widget1(request, owner, widget_name, widget_id):
    if NotionWidgets.objects.filter(widget_id=widget_id, user_id = owner).exists():
        ticker = request.POST['ticker']
        currency = request.POST['currency']

        name = ticker.upper()+'-'+currency
        ticker = ticker.lower()

        refreshRate = request.POST['Refreshrate']

        bg_color = request.POST['bg_color']
        if bg_color=="dark":
            bg_color='rgb(25,25,25)'
        else:
            bg_color='white'

        widget_object = NotionWidgets.objects.get(widget_id=widget_id)
        widget_object.name = name

        widget_object.widget_config['background_color'] = bg_color
        widget_object.widget_config['currency'] = currency
        widget_object.widget_config['hover_on'] = False
        widget_object.widget_config['refreshRate'] = refreshRate
        widget_object.widget_config['ticker'] = ticker

        widget_object.modified_at = current_DT()
        widget_object.save()

def config_widget2(request, owner, widget_name, widget_id):
    if NotionWidgets.objects.filter(widget_id=widget_id, user_id = owner).exists():
        bg_color = request.POST['bg_color']
        if bg_color=="dark":
            bg_color='rgb(25,25,25)'
            text_color = 'text-white'
        else:
            bg_color='white'
            text_color = 'text-black'
        
        widget_object = NotionWidgets.objects.get(widget_id=widget_id)
        widget_object.name = 'Fear & Greed Index'

        widget_object.widget_config['background_color'] = bg_color
        widget_object.widget_config['text_color'] = text_color

        widget_object.modified_at = current_DT()
        widget_object.save()

config_function_dict = {
    'widget1': config_widget1,
    'widget2': config_widget2
}


def widgetFunction3(request, widget):
    operation = request.POST['operation']
    if not -1<=int(operation)<=1:
        return {'status': False}
    
    if operation == 0:
        return {'status': True, 'count': widget.widget_config['count']}
    else:
        if widget.widget_config['count'] == 0 and operation == '-1':
            return {'status': True, 'count': 0}
        else:
            widget.widget_config['count'] += int(operation)
            widget.modified_at = current_DT()
            widget.save()
            return {'status': True, 'count': widget.widget_config['count']}

widget_function_dict = {
    'widget3': widgetFunction3
}

# Widget Counter
def add_widgets(widget_name, user_id):
    parent_id = UserCred.objects.get(user_id=user_id).id
    if WidgetsTracker.objects.filter(parent=parent_id).exists():
        user_record = WidgetsTracker.objects.get(parent=parent_id)
        if not user_record.widget_count.get(widget_name, None):
            user_record.widget_count[widget_name] = 0

        if user_record.widget_count[widget_name] < widgets_allowed_per_user.get(widget_name, 1):
            user_record.widget_count[widget_name]+=1
            user_record.modified_at = current_DT()
            user_record.save()
            return True
        else:
            return False
    else:
        WidgetsTracker(
            parent = UserCred.objects.get(user_id=user_id),
            widget_count = {},
            modified_at = current_DT()
        ).save()

        add_widgets(widget_name=widget_name, user_id=user_id)

            