from django.urls import path, include
from .views import *
from .widgetUpdateFuncs import add_widget1

urlpatterns = [
    path('', home),

    path('widget', widget),
    path('widget/<widget_id>', widget),

    path('config', configWidget),
    path('config/<widget_id>', configWidget),

    path('config/<widget_name>/<widget_id>', updateWidget),

    path('add', addWidget),
    path('delete/<widget_id>', deleteWidget),

    path('widget/update/<widget_id>', widgetFunctons)
]
