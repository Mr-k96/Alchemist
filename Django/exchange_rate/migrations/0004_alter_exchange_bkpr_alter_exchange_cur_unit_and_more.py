# Generated by Django 4.2.16 on 2024-11-22 04:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_rate', '0003_exchange_delete_exchangerate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchange',
            name='bkpr',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='cur_unit',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='deal_bas_r',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='kftc_bkpr',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='kftc_deal_bas_r',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='ten_dd_efee_r',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='ttb',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='tts',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='exchange',
            name='yy_efee_r',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=10, null=True),
        ),
    ]