from django.db import models

class EconomicNews(models.Model):
    title = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    date = models.DateTimeField()
    snippet = models.TextField()
    link = models.URLField()
    sentiment_score = models.IntegerField()
    country = models.CharField(max_length=10)  # 'KR' 또는 'US'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']