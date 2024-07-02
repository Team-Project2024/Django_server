from django.urls import path
from Chat import views; # chat에 있는 views를 가져옴

#여기에서 우리는 채팅의 인텐트 별로 요청을 받을거임 이건 스프링에서 판별해서 엔드포인트에 맞게 날릴거임

urlpatterns = [
    path('chat/course/query-recommend/',views.queryRecommend), # 질문 기반 과목 추천
    path('chat/course/history-recommend/',views.historyRecommend), # 수강 기록 기반 과목 추천
    path('chat/course/graduation-check/',views.graduationCheck), # 졸업요건 조회
    path('chat/hoseo/location/',views.hoseoLocation), # 졸업요건 조회
]
