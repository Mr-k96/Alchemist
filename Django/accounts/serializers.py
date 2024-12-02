from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from django.core.files.base import ContentFile
from PIL import Image
import base64
import uuid
import os
from .models import TermsAgreement

# 허용된 이미지 형식 및 최대 업로드 크기 설정
ALLOWED_IMAGE_TYPES = ['JPEG', 'JPG', 'PNG']
MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB

User = get_user_model()

def validate_image(image_data):
    """이미지 유효성 검사 및 처리"""
  
    if not image_data:
        return None

    try:
        # Base64 이미지 처리
        if isinstance(image_data, str) and 'data:image' in image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1].upper()

            if ext not in ALLOWED_IMAGE_TYPES:
                raise serializers.ValidationError(
                    f'지원되지 않는 이미지 형식입니다. 허용된 형식: {", ".join(ALLOWED_IMAGE_TYPES)}'
                )

            image_data = ContentFile(base64.b64decode(imgstr))
            img = Image.open(image_data)

        # 일반 파일 업로드 처리
        else:
            img = Image.open(image_data)
            if img.format not in ALLOWED_IMAGE_TYPES:
                raise serializers.ValidationError(
                    f'지원되지 않는 이미지 형식입니다. 허용된 형식: {", ".join(ALLOWED_IMAGE_TYPES)}'
                )

        # 이미지 크기 검증
        if image_data.size > MAX_UPLOAD_SIZE:
            raise serializers.ValidationError(
                f'이미지 크기는 {MAX_UPLOAD_SIZE / 1024 / 1024}MB를 초과할 수 없습니다.'
            )

        img.verify()
        return image_data

    except Exception as e:
        raise serializers.ValidationError(f'이미지 처리 중 오류가 발생했습니다: {str(e)}')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'avatar', 'date_of_birth']


class CustomRegisterSerializer(RegisterSerializer):
    date_of_birth = serializers.DateField(required=True)  # 생년월일 필드 추가

    avatar = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text='프로필 이미지 (JPEG/PNG, 최대 2MB)'
    )

    def validate_avatar(self, value):
        """프로필 이미지 유효성 검사"""
        print(value)
        return validate_image(value)

    def get_cleaned_data(self):
        """검증된 데이터 반환"""
        print('get')
        data = super().get_cleaned_data()
        data.update({
            'date_of_birth': self.validated_data.get('date_of_birth', ''),
            'avatar': self.validated_data.get('avatar', None)
        })
        return data

    def save(self, request):
        """사용자 저장 및 추가 정보 처리"""
        print('get')
        try:
            adapter = get_adapter()
            user = adapter.new_user(request)
            self.cleaned_data = self.get_cleaned_data()

            # 기본 사용자 정보 저장
            user = adapter.save_user(request, user, self, commit=False)

            # 추가 필드 저장 (생년월일과 프로필 이미지)
            if self.cleaned_data.get('date_of_birth'):
                user.date_of_birth = self.cleaned_data['date_of_birth']

            # 프로필 이미지 저장 처리
            image_data = self.cleaned_data.get('avatar')
            if image_data:
                if isinstance(image_data, str) and 'data:image' in image_data:
                    format, imgstr = image_data.split(';base64,')
                    ext = format.split('/')[-1]
                    file_name = f"{uuid.uuid4()}.{ext}"
                    image_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                    user.avatar = image_content
                else:
                    ext = os.path.splitext(image_data.name)[1]
                    file_name = f"{uuid.uuid4()}{ext}"
                    user.avatar.save(file_name, image_data, save=False)

            user.save()
            return user

        except Exception as e:
            raise serializers.ValidationError(f'사용자 저장 중 오류가 발생했습니다: {str(e)}')


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    date_of_birth = serializers.DateField(required=True)
    avatar = serializers.ImageField(
        required=False,
        allow_null=True,
        help_text='프로필 이미지 (JPEG/PNG, 최대 2MB)'
    )
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name',
                  'date_of_birth', 'avatar', 'avatar_url')
        read_only_fields = ('email',)

    def get_avatar_url(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

    def validate_avatar(self, value):
        return validate_image(value)

    def update(self, instance, validated_data):
        try:
            if 'avatar' in validated_data:
                if instance.avatar and os.path.exists(instance.avatar.path):
                    try:
                        os.remove(instance.avatar.path)
                    except OSError as e:
                        raise serializers.ValidationError(f'기존 이미지를 삭제하는 중 오류가 발생했습니다: {str(e)}')

                new_image = validated_data.pop('avatar')
                if new_image:
                    instance.avatar.save(new_image.name, new_image)

            return super().update(instance, validated_data)

        except Exception as e:
            raise serializers.ValidationError(f'프로필 업데이트 중 오류가 발생했습니다: {str(e)}')
        
# class CustomUserUpdateSerializer(serializers.ModelSerializer):
#     # date_of_birth = serializers.DateField(required=False)  # 생년월일 필드는 선택 사항으로 변경
#     # avatar = serializers.ImageField(
#     #     required=False,
#     #     allow_null=True,
#     #     help_text='프로필 이미지 (JPEG/PNG, 최대 2MB)'
#     # )

#     class Meta:
#         model = User
#         fields = ('email', 'date_of_birth', 'avatar')
    
#     def validate_avatar(self, value):
#         """프로필 이미지 유효성 검사"""
#         return validate_image(value)

#     def update(self, instance, validated_data):
#         """사용자 정보 업데이트"""
#         try:
#             if 'avatar' in validated_data:
#                 # 기존 이미지 삭제 처리
#                 if instance.avatar and os.path.exists(instance.avatar.path):
#                     try:
#                         os.remove(instance.avatar.path)
#                     except OSError as e:
#                         raise serializers.ValidationError(f'기존 이미지를 삭제하는 중 오류가 발생했습니다: {str(e)}')

#                 # 새 이미지 저장
#                 new_image = validated_data.pop('avatar', None)
#                 if new_image:
#                     instance.avatar.save(new_image.name, new_image)

#             # 다른 필드 업데이트
#             return super().update(instance, validated_data)

#         except Exception as e:
#             raise serializers.ValidationError(f'프로필 업데이트 중 오류가 발생했습니다: {str(e)}')


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','date_of_birth', 'avatar']


class TermsAgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAgreement
        fields = ['all_agreed', 'terms_of_service', 'privacy_policy']