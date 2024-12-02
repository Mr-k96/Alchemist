# models.py
from django.db import models

class DepositProduct(models.Model):
    fin_prdt_cd = models.CharField(max_length=100, unique=True) # 금융상품코드
    kor_co_nm = models.CharField(max_length=100) # 금융회사명
    fin_prdt_nm = models.CharField(max_length=100) # 금융상품명
    etc_note = models.CharField(max_length=1000) # 금융상품설명
    join_deny = models.IntegerField(null=True) # 가입제한
    join_member = models.CharField(max_length=100) # 가입대상
    join_way = models.CharField(max_length=100) # 가입방법
    spcl_cnd = models.CharField(max_length=100) # 우대조건
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='options') #외래키
    save_trm = models.IntegerField() #금융상품코드
    intr_rate = models.FloatField(null=True) #저축금리
    intr_rate2 = models.FloatField(null=True) #최고우대금리
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)