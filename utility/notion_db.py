import sys, datetime
sys.path.append('')
from notion.models import NotionWidgets

def fetch_user_widgets(user_id):
    return NotionWidgets.objects.filter(user_id=user_id)

def fetch_widget_congif(widget_id):
    if NotionWidgets.objects.filter(widget_id=widget_id).exists():
        notionWidgetConfig = NotionWidgets.objects.get(widget_id=widget_id)
        widget_name = notionWidgetConfig.widget_name
        widget_config = notionWidgetConfig.widget_config
        widget_config['name'] = notionWidgetConfig.name
        return widget_name, widget_config
    else:
        return None, None

def widget_owner_check(widget_id, owner):
    return NotionWidgets.objects.filter(widget_id=widget_id, user_id = owner).exists()