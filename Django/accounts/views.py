from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required


from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from django.contrib.auth import get_user_model


from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.core.exceptions import ValidationError
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer, CustomUserUpdateSerializer, TermsAgreementSerializer
from .models import TermsAgreement

User = get_user_model()

# def index(request):
#     users = User.objects.all()
#     context={
#         'users':users
#     }
#     return render(request, 'accounts/index.html', context)

# def login(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             return redirect('accounts:index')
#     else:
#         form = AuthenticationForm()
#     context = {
#         'form':form,
#     }
#     return render(request, 'accounts/login.html', context)
   
# def signup(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('accounts:index')
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)
@api_view(['GET'])
@login_required
def profile_view(request):
    user = get_object_or_404(User, username=request.user)
    serializer = CustomUserDetailsSerializer(user, context={'request': request})
    return Response(serializer.data)

@api_view(['PUT'])
@login_required
@parser_classes([MultiPartParser, FormParser])
def profile_update(request):
    user = get_object_or_404(User, username=request.user)
    serializer = CustomUserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        if 'avatar' in request.FILES:
            if user.avatar:
                user.avatar.delete(save=False)
        serializer.save()
        return Response(
            CustomUserDetailsSerializer(user, context={'request': request}).data,
            status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def register(request):
    """
    회원가입 API 엔드포인트
    
    처리 과정:
    1. 요청 데이터 유효성 검사
    2. 사용자 생성 및 추가 정보 저장
    3. 프로필 이미지 처리
    4. 응답 반환
    
    요청 데이터:
    - username: 사용자명 (필수)
    - email: 이메일 (필수)
    - password1: 비밀번호 (필수)
    - password2: 비밀번호 확인 (필수)
    - nickname: 닉네임 (선택)
    - profile_image: 프로필 이미지 파일 (선택)
    """

    try:
        with transaction.atomic():
            # 데이터 유효성 검사
            serializer = CustomRegisterSerializer(data=request.data)
   
            if not serializer.is_valid():
                return Response(
                    {'detail': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 사용자 생성
            user = serializer.save(request)
            
            # 응답 데이터 생성
            user_data = CustomUserDetailsSerializer(user).data
            
            # 절대 URL 생성 (이미지)
            if user_data.get('avatar'):
                user_data['avatar'] = request.build_absolute_uri(
                    user.avatar.url
                )
            
            return Response({
                'detail': '회원가입이 완료되었습니다.',
                'user': user_data
            }, status=status.HTTP_201_CREATED)
            
    except ValidationError as e:
        return Response({
            'detail': str(e),
            'code': 'validation_error'
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'detail': '회원가입 처리 중 오류가 발생했습니다.',
            'code': 'server_error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['POST'])
def terms_agreement(request):
    serializer = TermsAgreementSerializer(data=request.data)
    if serializer.is_valid():
        if serializer.validated_data['all_agreed']:
            # 여기서 사용자와 연결하거나 필요한 처리를 수행합니다.
            # 예: serializer.save(user=request.user)
            serializer.save()
            return Response({
                'detail': '약관에 동의하셨습니다.',
                'success': True
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'detail': '모든 약관에 동의해야 합니다.',
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)