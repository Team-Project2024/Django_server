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
    
    
# 챗봇 엔드포인트    
@csrf_exempt
def queryRecommend(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
    
        # 'content' 키로부터 값을 가져옴
        memberId = data.get('memberId')
        classification = data.get('classification')
        teamPlay = data.get('teamPlay')
        credit = data.get('credit')
        classMethod = data.get('classMethod')
        testType = data.get('testType')

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': memberId}
        return JsonResponse(response_data)
    
@csrf_exempt
def historyRecommend(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': data}
        return JsonResponse(response_data)
    
@csrf_exempt
def graduationCheck(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': data}
        return JsonResponse(response_data)
    
@csrf_exempt
def univEvent(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        memberId = data.get('memberId')
        month = data.get('month')

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': memberId}
        return JsonResponse(response_data)