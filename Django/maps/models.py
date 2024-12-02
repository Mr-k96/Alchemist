# models.py
from django.db import models

class Bank(models.Model):
    name = models.CharField(max_length=100)  # 은행 이름
    location = models.CharField(max_length=255, default='Unknown')  # 기본값 설정
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField()  # 경도