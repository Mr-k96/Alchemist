# serializers.py
from rest_framework import serializers
from .models import DepositProduct, DepositOption

class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'

class DepositProductSerializer(serializers.ModelSerializer):
    금리정보 = DepositOptionSerializer(many=True, source='options')
    금융상품코드 = serializers.CharField(source='fin_prdt_cd')
    금융회사명 = serializers.CharField(source='kor_co_nm')
    상품명 = serializers.CharField(source='fin_prdt_nm')
    
    class Meta:
        model = DepositProduct
        fields = '__all__'