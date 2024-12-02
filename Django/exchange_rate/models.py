from django.db import models

class Exchange(models.Model):
    cur_unit = models.CharField(max_length=10)  # 통화 단위
    cur_nm = models.CharField(max_length=100)   # 통화 이름
    ttb = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 송금 받으실 때 환율
    tts = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 송금 보내실 때 환율
    deal_bas_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 기준 환율
    bkpr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 매매 기준율
    yy_efee_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 연 이자율
    ten_dd_efee_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 10일 이자율
    kftc_deal_bas_r = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 한국 기준 환율
    kftc_bkpr = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)  # 한국 매매 기준율

    def __str__(self):
        return f"{self.cur_unit} ({self.cur_nm})"
