# ETF/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AssetInfo
from django.db.models import Q
import json


@csrf_exempt
def etf_list(request):
    if request.method == "GET":
        # GET 요청 처리
        queryset = AssetInfo.objects.all()
        data = list(queryset.values())
        return JsonResponse(data, safe=False)
        
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            queryset = AssetInfo.objects.all()
            
            # 기존 필터링 로직 유지
            if data.get("risks"):
                queryset = queryset.filter(risk_level__in=data["risks"])
            if data.get("markets"):
                queryset = queryset.filter(market_category__in=data["markets"])
                
            # 자산별 독립적인 필터링을 위한 Q 객체 생성
            asset_filters = Q()
            
            if data.get("assets"):
                for asset in data["assets"]:
                    if asset == "주식":
                        stock_filter = Q(asset_category="주식")
                        if data.get("stock_options"):
                            stock_filter &= Q(stock_options__in=data["stock_options"])
                        if data.get("industries"):
                            stock_filter &= (
                                Q(industry_1__in=data["industries"]) |
                                Q(industry_2__in=data["industries"]) |
                                Q(industry_3__in=data["industries"]) |
                                Q(industry_4__in=data["industries"])
                            )
                        asset_filters |= stock_filter
                        
                    elif asset == "채권":
                        bond_filter = Q(asset_category="채권")
                        if data.get("bond_options"):
                            bond_filter &= (
                                Q(bond_option1__in=data["bond_options"]) |
                                Q(bond_option2__in=data["bond_options"]) |
                                Q(bond_option3__in=data["bond_options"]) |
                                Q(bond_option4__in=data["bond_options"]) |
                                Q(bond_option5__in=data["bond_options"]) |
                                Q(bond_option6__in=data["bond_options"]) |
                                Q(bond_option7__in=data["bond_options"])
                            )
                        asset_filters |= bond_filter
                    else:
                        asset_filters |= Q(asset_category=asset)
                
                queryset = queryset.filter(asset_filters)

            data = list(queryset.values())
            return JsonResponse(data, safe=False)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
            
    return JsonResponse({"error": "Method not allowed"}, status=405)
