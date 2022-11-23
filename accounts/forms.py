from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Cliente, Empresa, Tags
import datetime as dt

YEARS_CHOICE = [str(i) for i in range(1940,2007)]
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

def only_digits(text):
    for i in text:
        try:
            int(i)
        except:
            return False
    return True

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
    
    def clean(self):
        cd = self.cleaned_data
        if not only_digits(cd.get('cpf')):
            self.add_error('cpf','Insira um CPF válido!')
        if not only_digits(cd.get('tel')):
            self.add_error('tel','Insira um telefone válido')
        return cd

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_cliente = True
        user.save()
        cliente = Cliente.objects.create(user = user,
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
    tags = forms.ModelMultipleChoiceField(
        queryset= Tags.objects.all(),
        required = True,
        widget = forms.CheckboxSelectMultiple
    )
    cnpj = forms.CharField(max_length=14,min_length=14,required=True)
    razao_social = forms.CharField(required=True)
    nome_fantasia = forms.CharField(required=True)
    tel = forms.CharField(min_length=10, max_length=11,required=True)
    endereco = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    image = forms.URLField(required=True)
    horario_inicio = forms.ChoiceField(choices= HOUR_CHOICES)
    horario_fim = forms.ChoiceField(choices=HOUR_CHOICES)
    seg = forms.BooleanField(required= False)
    ter = forms.BooleanField(required= False)
    qua = forms.BooleanField(required= False)
    qui = forms.BooleanField(required= False)
    sex = forms.BooleanField(required= False)
    sab = forms.BooleanField(required= False)
    dom = forms.BooleanField(required= False)
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows':'5','style':'resize: none;'}),required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        widgets = {'horario_inicio': forms.Select(choices=HOUR_CHOICES),
                    'horario_fim':forms.Select(choices=HOUR_CHOICES)}
    
    def clean(self):
        cd = self.cleaned_data
        if not only_digits(cd.get('cnpj')):
            self.add_error('cnpj','Insira um CNPJ válido')
        if not only_digits(cd.get('tel')):
            self.add_error('tel','Insira um Telefone válido')
        if not (cd.get('seg') or cd.get('ter') or cd.get('qua') or cd.get('qui') or cd.get('sex') or cd.get('sab') or cd.get('dom')):
            self.add_error('dom','Selecione ao menos um dia da semana!')
        if cd.get('horario_inicio') >= cd.get('horario_fim'):
            self.add_error('horario_inicio','O horário de Inicio deve ser menor que o Horário de Saida')
        return cd

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_empresa = True
        user.save()
        empresa = Empresa.objects.create(user = user,
                        cnpj = self.cleaned_data.get('cnpj'),
                        razao_social = self.cleaned_data.get('razao_social'),
                        nome_fantasia = self.cleaned_data.get('nome_fantasia'),
                        tel = self.cleaned_data.get('tel'),
                        email = self.cleaned_data.get('email'),
                        image = self.cleaned_data.get('image'),
                        endereco = self.cleaned_data.get('endereco'),
                        horario_inicio = self.cleaned_data.get('horario_inicio'),
                        horario_fim = self.cleaned_data.get('horario_fim'),
                        seg = self.cleaned_data.get('seg'),
                        ter = self.cleaned_data.get('ter'),
                        qua = self.cleaned_data.get('qua'),
                        qui = self.cleaned_data.get('qui'),
                        sex = self.cleaned_data.get('sex'),
                        sab = self.cleaned_data.get('sab'),
                        dom = self.cleaned_data.get('dom'),
                        desc = self.cleaned_data.get('desc')
                        )
        empresa.tags.add(*self.cleaned_data.get('tags'))
        return user
        
class EmpresaUpdate(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset= Tags.objects.all(),
        required = True,
        widget = forms.CheckboxSelectMultiple
    )
    tel = forms.CharField(min_length=10, max_length=11,required=True)
    endereco = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    image = forms.URLField(required=True)
    horario_inicio = forms.ChoiceField(choices= HOUR_CHOICES)
    horario_fim = forms.ChoiceField(choices=HOUR_CHOICES)
    seg = forms.BooleanField(required= False)
    ter = forms.BooleanField(required= False)
    qua = forms.BooleanField(required= False)
    qui = forms.BooleanField(required= False)
    sex = forms.BooleanField(required= False)
    sab = forms.BooleanField(required= False)
    dom = forms.BooleanField(required= False)
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows':'5','style':'resize: none;'}),required=False)

    class Meta:
        model = Empresa
        fields = ('tags','tel','endereco','email','image',
        'horario_inicio','horario_fim','seg','ter','qua','qui',
        'sex','sab','dom','desc')
        widgets = {'horario_inicio': forms.Select(choices=HOUR_CHOICES),
                    'horario_fim':forms.Select(choices=HOUR_CHOICES)}
    
    def clean(self):
        cd = self.cleaned_data
        if not only_digits(cd.get('tel')):
            self.add_error('tel','Insira um Telefone válido')
        if not (cd.get('seg') or cd.get('ter') or cd.get('qua') or cd.get('qui') or cd.get('sex') or cd.get('sab') or cd.get('dom')):
            self.add_error('dom','Selecione ao menos um dia da semana!')
        if cd.get('horario_inicio') >= cd.get('horario_fim'):
            self.add_error('horario_inicio','O horário de Inicio deve ser menor que o Horário de Saida')
        return cd

class ClienteUpdate(forms.ModelForm):
    email = forms.EmailField(required=True)
    image = forms.URLField(required=True)
    tel = forms.CharField(min_length=10, max_length=11,required=True)

    class Meta:
        model = Cliente
        fields = ('email','tel','image')
    
    def clean(self):
        cd = self.cleaned_data
        if not only_digits(cd.get('tel')):
            self.add_error('tel','Insira um telefone válido')
        return cd