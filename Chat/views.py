import json 
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F, ExpressionWrapper, FloatField
from .models import Member
from .models import UserChat
from .models import ChatBot
from .models import Major
from .models import GraduationRequirements
from .models import ConfirmCompletion
from .models import Lecture
from .models import CourseDetails
from .models import ChatRoom

logger = logging.getLogger(__name__)

"""
질문 기반 추천 기능:

이 기능은 사용자가 POST 요청을 통해 제공한 조건에 맞는 강의를 추천하는 기능
요청은 JSON 형식으로 이루어지며, 사용자는 다음과 같은 조건을 제공할 수 있다:
- classification: 강의 분류 (예: 전공, 일반교양 등)
- teamPlay: 팀 프로젝트 여부
- credit: 학점 수
- classMethod: 강의 방식 (예: 대면, 사이버, 하이브리드)
- testType: 시험 방식
- aiSw: AI.SW 마이크로디그리 이수 관련 여부

1. 요청 데이터 처리:
   사용자가 POST 요청을 통해 제공한 JSON 데이터를 수신하고, 이를 파싱하여 개별 조건을 추출한다.
   
2. Q 객체를 이용한 동적 필터링:
   Django의 Q 객체를 사용하여 여러 조건을 동적으로 결합한다.
   Q 객체는 AND 및 OR 연산자를 사용하여 복잡한 쿼리 논리를 구성할 수 있도록 도와준다.
   각 조건이 제공된 경우에만 해당 조건을 Q 객체에 추가하여 필터링한다.
   
3. 데이터베이스 조회:
   구성된 Q 객체를 사용하여 Lecture 모델에서 조건에 맞는 강의들을 조회한다.
   필터링된 강의들 중 강의평가 점수(course_evaluation)가 높은 순으로 정렬하여 상위 3개의 강의를 선택한다.

4. 결과 데이터 구성:
   선택된 강의들의 기본키(id)만 추출하여 리스트 형태로 변환한다.
   최종적으로 스프링 서버로 보낼 JSON 형식의 응답 데이터를 생성한다.
   이 응답 데이터는 'content' (추천 메시지), 'table' (조회된 테이블 이름), 'data' (추천된 강의들의 id 리스트)로 구성된다.

5. JSON 응답 반환:
   최종적으로 생성된 JSON 데이터를 스프링 서버로 반환하여, 사용자가 조건에 맞는 강의 추천 결과를 받을 수 있도록 한다.

이 메소드는 사용자의 질의 조건을 기반으로 데이터베이스에서 적절한 강의를 동적으로 필터링하고,
그 결과를 JSON 형식으로 반환하여 다른 서비스와의 연동을 원활하게 한다.
"""

@csrf_exempt
def queryRecommend(request):
    if request.method == 'POST':
        # JSON 파일에서 데이터 로드
        data = json.loads(request.body.decode('utf-8'))
        
        query = Q()
        if data.get('classification'):
            query &= Q(classification=data['classification'])
        if data.get('teamPlay'):
            query &= Q(team_play=data['teamPlay'])
        if data.get('credit'):
            query &= Q(credit=data['credit'])
        if data.get('classMethod'):
            query &= Q(class_method=data['classMethod'])
        if data.get('testType'):
            query &= Q(test_type=data['testType'])
        if 'aiswDegree' in data and data['aiswDegree'] is not None:
            query &= Q(ai_sw=data['aiswDegree'])
        
        # 데이터베이스에서 조건에 맞는 강의 조회하고 강의평가 점수가 높은 순으로 상위 3개 과목만 필터링
        top_lectures = Lecture.objects.filter(query).order_by('-course_evaluation')[:3]
        # 기본키(id)만 리스트 형태로 추출
        response_data = [lecture['id'] for lecture in list(top_lectures.values('id'))]
        
        # 스프링 서버로 보낼 JSON 데이터 생성
        result = {
            "content": "질문하신 항목에 맞는 과목 리스트입니다.",
            "table": "lecture",
            "data": response_data
        }
        
        return JsonResponse(result, safe=False)
    
"""
수강기록기반 과목 추천 기능:

이 기능은 회원의 수강기록을 바탕으로 부족한 역량을 채워줄 수 있는 강의를 추천한다.
요청은 POST 방식으로 이루어지며, JSON 형식의 데이터를 통해 회원 ID를 받는다:
- memberId: 추천을 받을 회원의 ID

1. 요청 데이터 처리:
   사용자가 POST 요청을 통해 제공한 JSON 데이터를 수신하고, 이를 파싱하여 회원 ID를 추출한다.

2. 회원의 TECH 현황 가져오기:
   member 테이블에서 해당 회원의 기록을 조회하여 현재 회원의 T(Teamwork), E(Entrepreneurship), C(Creative Thinking), H(Harnessing Resources) 현황을 가져온다.
   이 현황은 사용자가 수강한 모든 강의의 T, E, C, H 값의 총합이다.

3. 가중치 설정:
   회원의 현황에서 가장 높은 값을 기준으로 가중치를 설정한다.
   각 영역의 가중치는 max_value (가장 높은 값)에서 해당 영역의 현황 값을 뺀 값으로 설정된다.
   예를 들어, current_tech 값이 (14, 15, 19, 8)이라면, max_value는 19가 되고, 가중치는 T: 5, E: 4, C: 0, H: 11이 됩니다.

4. TECH 점수의 총합이 5인 강의 필터링:
   Lecture 테이블에서 TECH 점수의 총합이 5인 강의들만 필터링한다.
   이 필터링은 각 강의의 teamwork, entrepreneurship, creative_thinking, harnessing_resource 값의 합이 5인 강의들로 한정한다.

5. 가중치 기반 점수 계산:
   필터링된 강의들에 대해 가중치를 적용하여 점수를 계산한다.
   각 강의의 점수는 (teamwork * T 가중치) + (entrepreneurship * E 가중치) + (creative_thinking * C 가중치) + (harnessing_resource * H 가중치)로 계산된다.
   계산된 점수를 기준으로 강의들을 내림차순으로 정렬한다.

6. 상위 3개 강의 추천:
   가중치 기반 점수를 기준으로 상위 3개의 강의를 선택한다.

7. 결과 데이터 구성:
   추천된 강의들의 기본키(id)만 추출하여 리스트 형태로 변환한다.
   최종적으로 스프링 서버로 보낼 JSON 형식의 응답 데이터를 생성한다.
   이 응답 데이터는 'content' (추천 메시지), 'table' (조회된 테이블 이름), 'data' (추천된 강의들의 id 리스트)로 구성된다.

8. JSON 응답 반환:
   최종적으로 생성된 JSON 데이터를 스프링 서버로 반환하여, 사용자가 수강기록기반 과목 추천 결과를 받을 수 있도록 한다.

이 메소드는 회원의 수강기록을 기반으로 데이터베이스에서 적절한 강의를 동적으로 필터링하고,
그 결과를 JSON 형식으로 반환하여 다른 서비스와의 연동을 원활하게 한다.
"""

@csrf_exempt
def historyRecommend(request):
    if request.method == 'POST':
        # 요청에서 JSON 데이터 로드
        data = json.loads(request.body.decode('utf-8'))
        member_id = data
        # 회원의 TECH 현황 가져오기
        member = Member.objects.get(id=member_id)
        current_tech = {
            'T영역': member.teamwork,
            'E영역': member.entrepreneurship,
            'C영역': member.creative_thinking,
            'H영역': member.harnessing_resource,
        }

        if all(value == 0 for value in current_tech.values()):
            content = "아직 TECH 프로필이 없으니, 원하시는 강의 아무거나 들어보세요!"
            result = {
                "content": content,
                "table": "lecture",
                "data": []
            }
            return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
        
        # 가중치 설정 (최고점 기준 조정)
        max_value = max(current_tech.values())
        weights = {tech: max_value - current_tech[tech] for tech in current_tech}
        
        # TECH 점수의 총합이 5인 강의 필터링
        tech_courses = Lecture.objects.annotate(
            total_tech=F('teamwork') + F('entrepreneurship') + F('creative_thinking') + F('harnessing_resource')
        ).filter(total_tech=5)
        
        # 가중치 기반 점수 계산
        tech_courses = tech_courses.annotate(
            weighted_score=ExpressionWrapper(
                F('teamwork') * weights['T영역'] +
                F('entrepreneurship') * weights['E영역'] +
                F('creative_thinking') * weights['C영역'] +
                F('harnessing_resource') * weights['H영역'],
                output_field=FloatField()
            )
        ).order_by('-weighted_score')
        
        # 상위 3개 강의 추천
        top_courses = tech_courses[:3]
        
        # 추천된 과목들의 이유를 설명
        recommendation_reasons = []
        for course in top_courses:
            reason_parts = []
            if weights['T영역'] > 0 and course.teamwork > 0:
                reason_parts.append(f"T영역에 {course.teamwork}점")
            if weights['E영역'] > 0 and course.entrepreneurship > 0:
                reason_parts.append(f"E영역에 {course.entrepreneurship}점")
            if weights['C영역'] > 0 and course.creative_thinking > 0:
                reason_parts.append(f"C영역에 {course.creative_thinking}점")
            if weights['H영역'] > 0 and course.harnessing_resource > 0:
                reason_parts.append(f"H영역에 {course.harnessing_resource}점 ")
            recommendation_reason = f"{course.lecture_name}은(는) 부족한 부분인 " + ", ".join(reason_parts) + "을 채울 수 있어 추천되었습니다."
            recommendation_reasons.append(recommendation_reason)
        
        # 현재 사용자의 TECH 영역 현황 설명
        tech_status = ", ".join([f"{tech} {score}점" for tech, score in current_tech.items()])
        user_status = f"현재 사용자의 TECH 영역 현황은 {tech_status}입니다."
        second = "학생의 TECH 프로필 분석 결과, 추천드릴 수 있는 3가지 강의를 추천드리겠습니다."
        
        # 결과 데이터 구성
        content = f"{user_status} {second} " + " ".join(recommendation_reasons)
        
        result = {
            "content": content,
            "table": "lecture",
            "data": [course.id for course in top_courses]
        }
        
        return JsonResponse(result, safe=False, json_dumps_params={'ensure_ascii': False})
    
"""
함수명: graduationCheck
설명:
    이 함수는 학생의 학과, 트랙, 학번에 따른 졸업 요건을 확인하는 기능을 수행한다.
    POST 요청을 통해 학생의 ID를 받아, 현재 이수 현황을 가져오고,
    해당 학과와 학번에 맞는 졸업 요건과 비교하여 남은 학점을 반환한다.

단계:
1. POST 요청에서 JSON 데이터를 받아온다.
2. 제공된 학생 ID를 사용하여 Member 테이블에서 학생 정보를 조회한다.
3. 조회된 학생의 학과와 학번을 기준으로 GraduationRequirements 테이블에서 졸업 요건을 가져온다.
4. ConfirmCompletion 테이블에서 학생의 이수 학점을 조회한다.
5. 일반교양, 전공공통, 전공심화에서 초과된 학점을 계산하여 자유선택 학점으로 이동한다.
6. 졸업 요건과 비교하여 각 영역별 남은 학점을 계산한다.
7. 결과 데이터를 JSON 형식으로 구성하여 반환한다.

Postman 테스트 입력(Raw, Json)
{
    "memberId": "20193030"
}
"""


@csrf_exempt
def graduationCheck(request):
    if request.method == 'POST':
        # 요청에서 JSON 데이터 로드
        data = json.loads(request.body.decode('utf-8'))
        member_id = data
        
        # 회원 정보 조회
        member = Member.objects.get(id=member_id)
        major_id = member.major_id
        
        # 졸업 요건 조회
        graduation_requirements = GraduationRequirements.objects.get(major_id=major_id)
        
        # 이수 현황 조회
        completion = ConfirmCompletion.objects.get(member_id=member_id)
        
        # 초과 학점 계산
        excess_general_culture = max(0, completion.general_liberal_arts - graduation_requirements.general_liberal_arts)
        excess_major_common = max(0, completion.major_common - graduation_requirements.major_common)
        excess_major_advanced = max(0, completion.major_advanced - graduation_requirements.major_advanced)
        
        # 자유선택 학점으로 초과 학점 이동
        free_choice_with_excess = completion.free_choice + excess_general_culture + excess_major_common + excess_major_advanced
        
        # 부족한 학점 계산
        remaining_humanities = max(0, graduation_requirements.character_culture - completion.character_culture)
        remaining_basics = max(0, graduation_requirements.basic_liberal_arts - completion.basic_liberal_arts)
        remaining_general_culture = max(0, graduation_requirements.general_liberal_arts - completion.general_liberal_arts)
        remaining_major_common = max(0, graduation_requirements.major_common - completion.major_common)
        remaining_major_advanced = max(0, graduation_requirements.major_advanced - completion.major_advanced)
        remaining_free_choice = max(0, graduation_requirements.free_choice - free_choice_with_excess)
        total_completed_credits = (
                completion.character_culture +
                completion.basic_liberal_arts +
                completion.general_liberal_arts +
                completion.major_common +
                completion.major_advanced +
                completion.free_choice
            )
        # 결과 데이터 구성
        data = {
            "인성교양": remaining_humanities,
            "기초교양": remaining_basics,
            "일반교양": remaining_general_culture,
            "전공공통": remaining_major_common,
            "전공심화": remaining_major_advanced,
            "자유선택": remaining_free_choice,
            "졸업 총 학점": graduation_requirements.graduation_credits,
            "완료 학점": total_completed_credits
        }

        # 결과 데이터를 문자열로 변환
        content_string = ', '.join([f"{key}: {value}" for key, value in data.items()])
        
        # 최종 결과
        result = {
            "content": content_string,
            "table": "",
            "data": []
        }
        
        
        return JsonResponse(result, safe=False)


