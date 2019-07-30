
# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json


def chat(request):
    return render(request, 'chat/chat.html')
    
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
    
def main_chat(request,name):
    if request.is_ajax():
        if (request.method == 'POST'):
            response_data = {}
            post_text = request.POST.get('the_post')
            post = ChatLog(name=name , chat_text = post_text)
            post.save()
            response_data['name'] = name
            response_data['chat'] = post_text
            if 'tmp_id' in request.session:
                if (request.session['new_id'] == request.session['tmp_id']+1 ):
                    response_data['mycache'] = "normal"
                else:
                    response_data['mycache'] = "new message"
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            else :
                tmp_json = {}
                new_id = ChatLog.objects.order_by('-id')[0].id
                if 'new_id' in request.session :
                    request.session['tmp_id'] = request.session['new_id']
                    if (new_id == request.session['tmp_id']+1 ):
                        tmp_json['mycache'] = "normal"
                    else:
                        tmp_json['mycache'] = "new message"
                        diff = new_id - request.session['tmp_id']
                        tmp_json['diff'] = diff
                        while (diff > 0 ):
                            c = ChatLog.objects.get(id = request.session['tmp_id']+diff)
                            tmp_json["name"+repr(diff)] = c.name
                            tmp_json["new_msg"+ repr(diff)] = c.chat_text
                            diff -=1
                request.session['new_id'] = new_id
                tmp_json['new_id'] = new_id
                return HttpResponse(json.dumps(tmp_json), content_type="application/json")
    else:
        q = ChatLog.objects.all()
        return render(request, 'chat/main.html', {'chat': q, 'name':name })