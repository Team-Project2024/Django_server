from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 여기에서 데이터를 가져와서 사용하면 됨
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
    ######################################################################
    #################### 이 아래부터가 엔드 포인트 구분한거임 ####################
    ######################################################################
    
    
    ######################################################################
    ############################## 설명 ##################################
    #메서드에서 data를 받는 애들은 여러 데이터를 json으로 받는 애들이라 이걸 get으로 받아서 
    # 각 변수에 넣어둠 이걸 사용하면 됨  memberId로 받는것은 json으로 데이터를 받는 것이 아니라
    # memberId만을 전달받기 때문에 바로 memberId라는 변수에 저장해둠      
    # response_data에 spring 으로 전달해줄 데이터들을 Json으로 만들어서 보내주면 됨          
    #
    # response_data로 전달해줘야되는 데이터는
    # content -> 챗봇의 답변 내용
    # table -> 어떤 테이블에서 데이터를 긁어왔는지
    # data -> 사용한 데이터들(json)을 리스트에 담아서 보내주면 됨
    # data 예시 -> 강의 테이블에 있는 member_id로 member테이블에서 name을 가져와서 memberName에 넣고 member 테이블에 있는 major_id로 major에서 검색해서 department를 넣으면 됨
    # 이게 좀 어려우면 그냥 나한테 리스트로 pk값을 전달해주면 spring에서 처리할게
#     {
#     "content":"챗봇의 대답",
#     "table": "lecture",
#     "Data":[
#             {
#             "lectureId": 1,
#             "lectureName": "소프트웨어공학",
#             "classification": "전공공통",
#             "room": "2공 502호",
#             "credit": 3,
#             "division": 1,
#             "grade": 3,
#             "lectureTime": "목3,4",
#             "classMethod": "대면",
#             "testType": "실습,발표",
#             "teamwork": 1,
#             "entrepreneurship": 1,
#             "creativeThinking": 1,
#             "harnessingResource": 1,
#             "teamPlay": false,
#             "gradeMethod": "상대평가",
#             "aiSw": false,
#             "course_evaluation": 1,
#             "memberId": "201911",
#             "memberName": "안용학",
#             "department": "컴퓨터공학부"
#         },
#         {
#             "lectureId": 2,
#             "lectureName": "빅데이터컴퓨팅",
#             "classification": "전공공통",
#             "room": null,
#             "credit": 3,
#             "division": 1,
#             "grade": 4,
#             "lectureTime": "목2,3 금11",
#             "classMethod": "대면",
#             "testType": "클로즈북",
#             "teamwork": 1,
#             "entrepreneurship": 1,
#             "creativeThinking": 1,
#             "harnessingResource": 1,
#             "teamPlay": false,
#             "gradeMethod": "상대평가",
#             "testMethod": "필기,실기",
#             "aiSw": false,
#             "course_evaluation": 1,
#             "memberId": "000011",
#             "memberName": "홍충표",
#             "department": "컴퓨터공학부"
#         }
#     ]
# }
    
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
        aiSw = data.get('aiSw')
        print(classification + " " + str(teamPlay) + " " + credit + " " + classMethod + " " + testType + " " + str(aiSw))

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': memberId}
        return JsonResponse(response_data)
    
@csrf_exempt
def historyRecommend(request):
    if request.method == 'POST':
        memberId = json.loads(request.body.decode('utf-8'))
        print(memberId)

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': memberId}
        return JsonResponse(response_data)
    
@csrf_exempt
def graduationCheck(request):
    if request.method == 'POST':
        memberId = json.loads(request.body.decode('utf-8'))
        print(memberId)

        # 가져온 값을 JSON 응답으로 반환
        response_data = {'memberId': memberId}
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