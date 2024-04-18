from django.db import models

class UserChat(models.Model):
    id = models.AutoField(primary_key=True)
    member_id = models.CharField(max_length=20)
    chat_date = models.DateTimeField()
    content = models.TextField()

    class Meta:
        db_table = 'user_chat'
        app_label = 'Chat'

class ChatBot(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    user_chat = models.ForeignKey(UserChat, on_delete=models.CASCADE, db_column='user_chat_id')

    class Meta:
        db_table = 'chat_bot'
        app_label = 'Chat'

class Member(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=45)
    role = models.CharField(max_length=45)
    major = models.CharField(max_length=45)

    class Meta:
        db_table = 'member'
        app_label = 'Chat'