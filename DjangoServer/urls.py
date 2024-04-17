from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Chat.urls')), # 챗으로 들어오면 Chat.urls로 권한 위임
]
