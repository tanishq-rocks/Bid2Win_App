# Generated by Django 3.0.2 on 2020-01-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('biddd', '0004_auto_20200108_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winners',
            name='winning_product_name',
            field=models.CharField(default='0', max_length=20),
        ),
        migrations.AlterField(
            model_name='winners',
            name='winning_product_price',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
