from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member
from .models import UserChat
from .models import ChatBot

import json

# 최종적으로는 스프링으로부터 학번, 엔티티를 받아서
# 추천에 대한 값을 받아서 반환해줘야됨
# 이건 메소드에서 전달해주는거 그대로 전달해주면 됨

@csrf_exempt
def index(request):
    if request.method == 'POST':
        # 전송된 JSON 데이터 파싱
        data = json.loads(request.body.decode('utf-8'))
        
        # 'content' 키로부터 값을 가져옴
        content = data.get('content')

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'result': content}
        return JsonResponse(response_data)

@csrf_exempt
def getMember(request):
    if request.method == 'GET':
        members = Member.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(members.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getChatUser(request):
    if request.method == 'GET':
        userchats = UserChat.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(userchats.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getChatBot(request):
    if request.method == 'GET':
        chatbots = ChatBot.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(chatbots.values())
        return JsonResponse(data, safe=False)