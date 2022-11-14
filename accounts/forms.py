from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Cliente, Empresa
from dise import settings
import datetime as dt

YEARS_CHOICE = [str(i) for i in range(1940,2007)]
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]


class ClienteSignUpForm(UserCreationForm):
    cpf = forms.CharField(max_length=11,min_length=11,required=True)
    nome = forms.CharField(required=True)
    sobrenome = forms.CharField(required=True)
    tel = forms.CharField(min_length=10, max_length=11,required=True)
    nascimento = forms.DateField(required=True,label='Data de Nascimento', widget=forms.SelectDateWidget(years=YEARS_CHOICE))
    email = forms.EmailField(required=True)
    image = forms.URLField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_cliente = True
        user.save()
        cliente = Cliente(user = user,
                        cpf = self.cleaned_data.get('cpf'),
                        nome = self.cleaned_data.get('nome'),
                        sobrenome = self.cleaned_data.get('sobrenome'),
                        tel = self.cleaned_data.get('tel'),
                        nascimento = self.cleaned_data.get('nascimento'),
                        email = self.cleaned_data.get('email'),
                        image = self.cleaned_data.get('image')
                        )
        return user

class EmpresaSignUpForm(UserCreationForm):
    cnpj = forms.CharField(max_length=14,min_length=14,required=True)
    razao_social = forms.CharField(required=True)
    nome_empresa = forms.CharField(required=True)
    tel = forms.CharField(min_length=10, max_length=11,required=True)
    enderco = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    image = forms.URLField(required=True)
    seg = forms.BooleanField()
    ter = forms.BooleanField()
    qua = forms.BooleanField()
    qui = forms.BooleanField()
    sex = forms.BooleanField()
    sab = forms.BooleanField()
    dom = forms.BooleanField()

    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {'horario_inicio': forms.Select(choices=HOUR_CHOICES),
                    'horario_fim':forms.Select(choices=HOUR_CHOICES)}
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_empresa = True
        user.save()
        cliente = Empresa(user = user,
                        cnpj = self.cleaned_data.get('cnpj'),
                        razao_social = self.cleaned_data.get('razao_social'),
                        nome_empresa = self.cleaned_data.get('nome_empresa'),
                        tel = self.cleaned_data.get('tel'),
                        email = self.cleaned_data.get('email'),
                        image = self.cleaned_data.get('image'),
                        seg = self.cleaned_data.get('seg'),
                        ter = self.cleaned_data.get('ter'),
                        qua = self.cleaned_data.get('qua'),
                        qui = self.cleaned_data.get('qui'),
                        sex = self.cleaned_data.get('sex'),
                        sab = self.cleaned_data.get('sab'),
                        dom = self.cleaned_data.get('dom'),
                        )
        return user
        
