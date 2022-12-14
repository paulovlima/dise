# Generated by Django 3.2.16 on 2022-11-28 00:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0005_auto_20221124_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='servico',
            name='orcamento',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='servico',
            name='data_agendada',
            field=models.DateField(default=datetime.date(2022, 11, 27)),
        ),
    ]
