from django.db import models

# Django에서 필요한 테이블 
    # 1. 전공 ,사용자 테이블(사용자 정보가 필요한 경우 조회)
    # 2. 졸업요건, 교내행사, 강의 테이블 (학습을 위해 필요, 대신 직접 수정 및 추가는 안함 스프링에서 바로 해버릴거임 관리자 권한으로)

class Major(models.Model):
    major_id = models.AutoField(primary_key=True)
    department = models.CharField(max_length=45)
    track = models.CharField(max_length=45)

    class Meta:
        db_table = 'major'
        app_label = 'major'

class GraduationRequirements(models.Model):
    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=20)
    character_culture = models.IntegerField()
    basic_liberal_arts = models.IntegerField()
    general_liberal_arts = models.IntegerField()
    msc = models.IntegerField()
    major_common = models.IntegerField()
    major_advanced = models.IntegerField()
    free_choice = models.IntegerField()
    graduation_credits = models.IntegerField()
    volunteer = models.IntegerField()
    chapel = models.IntegerField()
    major_id = models.ForeignKey(Major, on_delete=models.CASCADE, db_column='major_id')

    class Meta:
        db_table = 'graduation_requirements'
        app_label = 'graduation_requirements'

class Member(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    teamwork = models.IntegerField()
    entrepreneurship = models.IntegerField()
    creative_thinking = models.IntegerField()
    harnessing_resource = models.IntegerField()
    major_id = models.ForeignKey(Major, on_delete=models.CASCADE, db_column='major_id')

    class Meta:
        db_table = 'member'
        app_label = 'member'

class ConfirmCompletion(models.Model):
    id = models.AutoField(primary_key=True)
    character_culture = models.IntegerField()
    basic_liberal_arts = models.IntegerField()
    general_liberal_arts = models.IntegerField()
    major_common = models.IntegerField()
    major_advanced = models.IntegerField()
    free_choice = models.IntegerField()
    graduation_credits = models.IntegerField()
    volunteer = models.IntegerField()
    chapel = models.IntegerField()
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')

    class Meta:
        db_table = 'confirm_completion'
        app_label = 'confirm_completion'

class ChatRoom(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    last_chat_date = models.DateTimeField()
    first_chat = models.CharField(max_length=255)

    class Meta:
        db_table = 'chat_room'
        app_label = 'chat_room'

class UserChat(models.Model):
    id = models.AutoField(primary_key=True)
    chat_date = models.DateTimeField()
    content = models.TextField()
    room_id = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, db_column='room_id')

    class Meta:
        db_table = 'user_chat'
        app_label = 'user_chat'

class ChatBot(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    user_chat_id = models.ForeignKey(UserChat, on_delete=models.CASCADE, db_column='user_chat_id')

    class Meta:
        db_table = 'chat_bot'
        app_label = 'chat_bot'

class Lecture(models.Model):
    id = models.AutoField(primary_key=True)
    lecture_name = models.CharField(max_length=100)
    classification = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    credit = models.IntegerField()
    division = models.IntegerField()
    grade = models.IntegerField()
    lecture_time = models.CharField(max_length=20)
    ai_sw = models.BooleanField()
    class_method = models.CharField(max_length=20)
    test_type = models.CharField(max_length=30)
    teamwork = models.IntegerField()
    entrepreneurship = models.IntegerField()
    creative_thinking = models.IntegerField()
    harnessing_resource = models.IntegerField()
    team_play = models.BooleanField()
    grade_method = models.CharField(max_length=20)
    course_evaluation = models.IntegerField()
    introduction = models.CharField(max_length=255)
    grade_ratio = models.CharField(max_length=255)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')

    class Meta:
        db_table = 'lecture'
        app_label = 'lecture'

class CourseDetails(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column='member_id')
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='lecture_id')
    grade = models.CharField(max_length=10)

    class Meta:
        db_table = 'course_details'
        app_label = 'course_details'

class SchoolEvent(models.Model):
    id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=30)
    event_period = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    is_canceled = models.BooleanField()
    modified = models.BooleanField()

    class Meta:
        db_table = 'school_event'
        app_label = 'school_event'
        
class Lecture_detail(models.Model):
    id = models.AutoField(primary_key=True)
    week = models.IntegerField()
    content = models.CharField(max_length=255)
    lecture_id = models.ForeignKey(Lecture, on_delete=models.CASCADE, db_column='lecture_id')

    class Meta:
        db_table = 'lecture_detail'
        app_label = 'lecture_detail'