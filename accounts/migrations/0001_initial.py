# Generated by Django 3.2.16 on 2022-11-12 20:48

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_empresa', models.BooleanField(default=False)),
                ('is_cliente', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('nome', models.CharField(max_length=40)),
                ('sobrenome', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=11, unique=True)),
                ('nascimento', models.DateField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('image', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('razao_social', models.CharField(max_length=200)),
                ('cnpj', models.IntegerField(unique=True)),
                ('horario_inicio', models.TimeField()),
                ('horario_fim', models.TimeField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('tel', models.CharField(max_length=11, unique=True)),
                ('endereco', models.CharField(max_length=150)),
                ('nome_empresa', models.CharField(max_length=50)),
                ('image', models.URLField()),
                ('dom', models.BooleanField(default=False)),
                ('seg', models.BooleanField(default=False)),
                ('ter', models.BooleanField(default=False)),
                ('qua', models.BooleanField(default=False)),
                ('qui', models.BooleanField(default=False)),
                ('sex', models.BooleanField(default=False)),
                ('sab', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('empresa', models.ManyToManyField(to='accounts.Empresa')),
            ],
        ),
    ]
