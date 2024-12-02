# serializers.py
from rest_framework import serializers
from .models import AssetInfo

class AssetInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetInfo
        fields = '__all__'
        
    def validate_risk_level(self, value):
        # 위험도 유효성 검사 로직
        valid_risk_levels = ['1', '2', '3', '4', '5', '6']
        if value not in valid_risk_levels:
            raise serializers.ValidationError("유효하지 않은 위험도입니다.")
        return value