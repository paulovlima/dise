# Generated by Django 3.2.16 on 2022-11-28 01:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agendamento', '0006_auto_20221127_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servico',
            name='orcamento',
        ),
    ]
