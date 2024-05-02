from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member
from .models import UserChat
from .models import ChatBot
from .models import Major
from .models import GraduationRequirements
from .models import ConfirmCompletion
from .models import Lecture
from .models import CourseDetails
from .models import SchoolEvent
from .models import ChatRoom

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
    
@csrf_exempt
def getMajor(request):
    if request.method == 'GET':
        major = Major.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(major.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getGraduationRequirements (request):
    if request.method == 'GET':
        graduation_requirements = GraduationRequirements.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(graduation_requirements.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getconfirmCompletion (request):
    if request.method == 'GET':
        confirm_completion = ConfirmCompletion.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(confirm_completion.values())
        return JsonResponse(data, safe=False)

    
@csrf_exempt
def getLecture(request):
    if request.method == 'GET':
        lecture = Lecture.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(lecture.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getCourseDetails(request):
    if request.method == 'GET':
        course_details = CourseDetails.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(course_details.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getSchoolEvent(request):
    if request.method == 'GET':
        school_event = SchoolEvent.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(school_event.values())
        return JsonResponse(data, safe=False)
    
@csrf_exempt
def getChatRoom(request):
    if request.method == 'GET':
        room = ChatRoom.objects.all()
        # QuerySet을 JSON 형태로 변환하여 반환
        data = list(room.values())
        return JsonResponse(data, safe=False)
    