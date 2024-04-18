from django.urls import path
from Chat import views; # chat에 있는 views를 가져옴

#여기에서 우리는 채팅의 인텐트 별로 요청을 받을거임 이건 스프링에서 판별해서 엔드포인트에 맞게 날릴거임

urlpatterns = [
    path('chat/member/',views.getMember), # DB Member 테이블 GET 테스트
    path('chat/user/',views.getChatUser), # DB useChat 테이블 GET 테스트
    path('chat/getChatBot/',views.getChatBot) # DB chatbot 테이블 GET 테스트
]
