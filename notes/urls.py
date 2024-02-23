from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home),
    path('create', create_note),
    path('update', update_note),
    path('toggle_pin/<note_id>', update_pin_status),
    path('delete/<note_id>', delete_note),
    path('download/<note_id>', download_note_as_txt),
    path('sharable', make_note_sharable),
    path('s/<note_id>', shared_note)
]
