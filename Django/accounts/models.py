# models.py
from django.contrib.auth.models import AbstractUser  # Django의 기본 사용자 모델을 확장하기 위해 임포트
from django.db import models  # Django의 모델 클래스와 필드를 사용하기 위해 임포트

# 사용자 모델을 확장하기 위한 커스텀 User 모델 정의
class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # 프로필 이미지 필드, 업로드 경로 지정
    date_of_birth = models.DateField(blank=True, null=True)  # 생년월일 필드 추가, 비어 있을 수 있음

    def __str__(self):
        return self.username

# # 사용자 프로필 정보를 저장하는 Profile 모델 정의
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)  # User 모델과 일대일 관계 설정
#     bio = models.TextField(blank=True)  # 사용자 소개를 위한 텍스트 필드, 비어 있을 수 있음
#     avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # 프로필 이미지 필드, 업로드 경로 지정
#     email = models.EmailField(blank=True)  # 이메일 필드 추가, 비어 있을 수 있음
#     date_of_birth = models.DateField(blank=True, null=True)  # 생년월일 필드 추가, 비어 있을 수 있음

#     def __str__(self):
#         return self.user.username  # 객체를 문자열로 표현할 때 사용자 이름 반환

# 약관동의
class TermsAgreement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    all_agreed = models.BooleanField(default=False)
    terms_of_service = models.BooleanField(default=False)
    privacy_policy = models.BooleanField(default=False)
    agreed_at = models.DateTimeField(auto_now_add=True)