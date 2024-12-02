from django.db import models

class AssetInfo(models.Model):
    # 단축코드: 고유 식별 코드 (예: 문자열)
    short_code = models.CharField(max_length=20, unique=True)

    # 한글종목약명: 종목 이름 (예: 문자열)
    name = models.CharField(max_length=100)

    # 기초시장분류: 시장 분류 정보 (예: 문자열)
    market_category = models.CharField(max_length=50, null=True, blank=True)

    # 기초자산분류: 자산 분류 정보 (예: 문자열)
    asset_category = models.CharField(max_length=50, null=True, blank=True)

    # 대표지수: 기본 값 (예: 문자열)
    default = models.CharField(max_length=20, null=True, blank=True)

    # 옵션 표기: 옵션 정보 (예: 문자열)
    stock_options = models.CharField(max_length=20, null=True, blank=True)

    # 채권 옵션: 자산 분류 정보(예: 문자열)
    bond_option1 = models.CharField(max_length=20, null=True, blank=True)
    bond_option2 = models.CharField(max_length=20, null=True, blank=True)
    bond_option3 = models.CharField(max_length=20, null=True, blank=True)
    bond_option4 = models.CharField(max_length=20, null=True, blank=True)
    bond_option5 = models.CharField(max_length=20, null=True, blank=True)
    bond_option6 = models.CharField(max_length=20, null=True, blank=True)
    bond_option7 = models.CharField(max_length=20, null=True, blank=True)

    # 산업1 ~ 산업4: 산업 분류 단계 (예: 문자열)
    industry_1 = models.CharField(max_length=50, null=True, blank=True)
    industry_2 = models.CharField(max_length=50, null=True, blank=True)
    industry_3 = models.CharField(max_length=50, null=True, blank=True)
    industry_4 = models.CharField(max_length=50, null=True, blank=True)

    # 위험도: 위험 등급 (예: 정수형 또는 문자열)
    risk_level = models.CharField(max_length=20)

    # 운용사: 운용사 이름 (예: 문자열)
    manager = models.CharField(max_length=100)

    def __str__(self):
        return self.name