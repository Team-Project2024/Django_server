from django.urls import path
from Chat import views; # chat에 있는 views를 가져옴

#여기에서 우리는 채팅의 인텐트 별로 요청을 받을거임 이건 스프링에서 판별해서 엔드포인트에 맞게 날릴거임

urlpatterns = [
    path('chat/',views.get) #chat으로 요청이 들어오면 chat폴더 view파일에 있는 index라는 함수 호출
]
