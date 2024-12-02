import csv
from django.core.management.base import BaseCommand
from ETF.models import AssetInfo

class Command(BaseCommand):
    help = "Import asset information from a CSV file"

    def handle(self, *args, **kwargs):
        file_path = 'ETF/management/commands/asset_info.csv'  # CSV 파일 경로

        # UTF-8 BOM 처리
        with open(file_path, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            asset_list = []

            for row in reader:
                asset = AssetInfo(
                    short_code=row['short_code'],  # 헤더와 Django 필드 이름이 일치해야 함
                    name=row['name'],
                    market_category=row.get('market_category'),
                    asset_category=row.get('asset_category'),
                    default=row.get('default'),
                    stock_options=row.get('stock_options'),
                    bond_option1=row.get('bond_option1'),
                    bond_option2=row.get('bond_option2'),
                    bond_option3=row.get('bond_option3'),
                    bond_option4=row.get('bond_option4'),
                    bond_option5=row.get('bond_option5'),
                    bond_option6=row.get('bond_option6'),
                    bond_option7=row.get('bond_option7'),
                    industry_1=row.get('industry_1'),
                    industry_2=row.get('industry_2'),
                    industry_3=row.get('industry_3'),
                    industry_4=row.get('industry_4'),
                    risk_level=row['risk_level'],
                    manager=row['manager']
                )
                asset_list.append(asset)

            # Bulk create for performance
            AssetInfo.objects.bulk_create(asset_list)

        self.stdout.write(self.style.SUCCESS('Successfully imported asset information!'))

# 엑셀 파일 DB에 저장하는 명령어
# python manage.py import_asset_info