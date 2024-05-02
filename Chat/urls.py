from django.urls import path
from Chat import views; # chat에 있는 views를 가져옴

#여기에서 우리는 채팅의 인텐트 별로 요청을 받을거임 이건 스프링에서 판별해서 엔드포인트에 맞게 날릴거임

urlpatterns = [
    path('member/',views.getMember), # DB Member 테이블 GET 테스트
    path('chat/user/',views.getChatUser), # DB useChat 테이블 GET 테스트
    path('chat/getChatBot/',views.getChatBot), # DB chatbot 테이블 GET 테스트
    path('major/',views.getMajor), # DB major 테이블 GET 테스트
    path('graduation_requirements/',views.getGraduationRequirements), # DB graduation_requirements 테이블 GET 테스트
    path('confirm_completion/',views.getconfirmCompletion), # DB confirm_completion 테이블 GET 테스트
    path('lecture/',views.getLecture), # DB lecture 테이블 GET 테스트
    path('course_details/',views.getCourseDetails), # DB course_details 테이블 GET 테스트
    path('school_event/',views.getSchoolEvent), # DB school_event 테이블 GET 테스트
    path('chat-room/',views.getChatRoom), # DB room 테이블 GET 테스트
]
