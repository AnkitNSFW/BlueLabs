from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.http import HttpResponse, JsonResponse
from .models import notes
# Create your views here.
import sys
sys.path.append('')
from app.models import UserCred
from utility.assests_links import asset_urls
from utility.app_db import check_login_status
from utility.utility_func import create_uuid, check_uuid4, current_DT


def home(request):
    user_data = check_login_status(request)
    if not user_data:
        return redirect('/')
    context = {}
    context['asset_urls'] = asset_urls
    context['notes'] = {'pinned': [], "unpinned": []}
    user_notes = notes.objects.filter(parent=UserCred.objects.get(user_id=user_data['user_id']))
    for user_note in user_notes:
        note_json_content = {"note_id": user_note.note_id,
                "update_request_no": user_note.update_request_no+1,
                    "title": user_note.title,
                    "note": user_note.note,
                    "pinned": user_note.pinned,
                    "modified_at": user_note.modified_at.strftime('%d-%m-%Y %H:%M:%S')}
        if user_note.pinned:
            context['notes']['pinned'].append(note_json_content)
        else:
            context['notes']['unpinned'].append(note_json_content)
        
    return render(request, 'notes/home.html', context=context)


def create_note(request):
    user_data = check_login_status(request)
    if not user_data:
        return JsonResponse({'status': False})
    new_note_uuid = create_uuid()
    current_date_time = current_DT()
    notes(parent=UserCred.objects.get(user_id=user_data['user_id']),
          note_id = new_note_uuid,
          update_request_no = 0,
          title = '',
          note = '',
          pinned = False,
          created_at = current_date_time,
          modified_at = current_date_time
          ).save()
    
    return JsonResponse({'status': True, 'note_id': new_note_uuid, 'created_at': current_date_time.strftime('%d-%m-%Y %H:%M:%S'), 'update_request_no': 0})


@require_POST
@csrf_exempt
def update_note(request):
    user_data = check_login_status(request)
    if not user_data:
        return JsonResponse({'status': False, 'msg': 'Login or use proper credentials for sending updates/changes'})

    if request.POST.get('note_id', None) and request.POST.get('update_request_no', None) and (isinstance(request.POST.get('title', None) ,str) and isinstance(request.POST.get('note', None) ,str)):
        if notes.objects.filter(note_id = request.POST['note_id'] ).exists():
            Note = notes.objects.get(note_id=request.POST['note_id'])
            if Note.update_request_no < int(request.POST['update_request_no']):
                if isinstance(request.POST.get('title', None) ,str):
                    Note.title = request.POST['title']
                if isinstance(request.POST.get('note', None) ,str):
                    Note.note = request.POST['note']

                Note.modified_at = current_DT()
                Note.update_request_no +=1
                Note.save()
            return JsonResponse({'status': True, 'modified_at': Note.modified_at.strftime('%d-%m-%Y %H:%M:%S'),  'update_request_no': Note.update_request_no+1})

    return JsonResponse({'status': False, 'msg': "request didn't had all the required data. Contact the developer to know the Docs"})


def update_pin_status(request, note_id):
    user_data = check_login_status(request)
    if not user_data:
        return JsonResponse({'status': False, 'msg': 'Login or use proper credentials for sending updates/changes'})
    
    if notes.objects.filter(note_id = note_id ).exists():
        Note = notes.objects.get(note_id=note_id)
        Note.pinned = not Note.pinned
        Note.modified_at = current_DT()
        Note.save()
        return JsonResponse({'status': True, 'current_pin_status': Note.pinned})
    else:
        return JsonResponse({'status': False, 'msg': "The Note you are trying to pin/unpin don't exist."})


def delete_note(request, note_id):
    user_data = check_login_status(request)
    if not user_data:
        return JsonResponse({'status': False, 'msg': 'Login or use proper credentials for sending updates/changes'})
    
    if notes.objects.filter(note_id = note_id ).exists():
        notes.objects.get(note_id=note_id).delete()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'msg': "The Note you are trying to delete don't exist."})


def download_note_as_txt(request, note_id):
    user_data = check_login_status(request)
    if not user_data:
        return JsonResponse({'status': False, 'msg': 'Login or use proper credentials to download Notes as .txt file.'})
    
    if notes.objects.filter(note_id = note_id ).exists():
        Note = notes.objects.get(note_id=note_id)
        filename = f"{user_data['first_name']}-{note_id}.txt"
        content = f"Title: {Note.title}\n\n"
        content += Note.note.replace('<br>','\n')
        content += f"\n\n\nCreated on: {Note.created_at}\nLast modified at: {Note.modified_at} (as of {current_DT().strftime('%d-%m-%Y %H:%M:%S')} UTC)\nPinned: {Note.pinned}\nNote_id: {Note.note_id}\nNumber of time updated: {Note.update_request_no}"
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    else:
        return JsonResponse({'status': False, 'msg': "The Note you are trying to download as .txt don't exist."})

@require_POST
@csrf_exempt
def make_note_sharable(request):
    user_data = check_login_status(request)
    if not user_data:
        return JsonResponse({'status': False, 'msg': 'Login-to-share'})
    
    note_id = request.POST.get('note_id', None)
    if note_id:
        if notes.objects.filter(note_id=note_id).exists():
            note = notes.objects.get(note_id=note_id)
            note.shared = True
            note.save()
            return JsonResponse({'status': True})
    
    return JsonResponse({'status': False, 'msg': "Error"})


def shared_note(request, note_id):
    context = {}
    context['asset_urls'] = asset_urls

    # When a new note is created the note_id which we return using the API don't have the "-" ("-" appears when the page is refreshed)
    # so if user create and then directly share the note the note_id wothout "-" is handled
    if '-' not in note_id:
        note_id = note_id[:8] + '-' + note_id[8:12] + '-' + '4' + note_id[13:16] + '-' + note_id[16:20] + '-' + note_id[20:]

    if not check_uuid4(note_id):
        context['note_exist'] = False
        context['msg'] = "The note you are trying to access do not exist or have been deleted."
        return render(request, 'notes/shared_note.html', context=context)
    
    if notes.objects.filter(note_id=note_id).exists():
        context['note_exist'] = True
        Note = notes.objects.get(note_id=note_id)
        if Note.shared:
            context['note_shared'] = True
            context['title'] = Note.title
            context['note'] = Note.note
        else:
            context['note_shared'] = False
            context['msg'] = "Sharing is disabled for this note."
    else:
        context['note_exist'] = False
        context['msg'] = "The note you are trying to access do not exist or have been deleted."
        
    return render(request, 'notes/shared_note.html', context=context)
    
