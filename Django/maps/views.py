import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Bank
from .serializers import BankSerializer

# 환경 변수 로드
load_dotenv()

@api_view(['GET'])
def get_nearby_banks(request):
    city = request.query_params.get('city')
    bank_name = request.query_params.get('bank')

    # 유효성 검사
    if not city or not bank_name:
        return Response({"error": "city and bank parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 데이터베이스 쿼리
        banks = Bank.objects.filter(location__icontains=city, name__icontains=bank_name)

        if not banks.exists():
            return Response({"message": "No banks found matching the criteria."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BankSerializer(banks, many=True)
        
        # 응답 데이터에 추가 정보 포함
        return Response({
            "requested_city": city,
            "requested_bank": bank_name,
            "banks": serializer.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)