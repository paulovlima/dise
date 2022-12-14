# Generated by Django 3.2.16 on 2022-11-12 21:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orcamento', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('hora_agendada', models.DateTimeField()),
                ('endereco_agendado', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_pagar', models.DecimalField(decimal_places=2, default=0, max_digits=4)),
                ('status', models.CharField(max_length=200)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cliente')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.empresa')),
                ('servico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agendamento.servico', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.DecimalField(decimal_places=2, default=5, max_digits=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='CommentCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('rating', models.DecimalField(decimal_places=2, default=5, max_digits=2)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.cliente')),
            ],
        ),
    ]
