from django import forms
from accounts.models import *
from .models import Servico, Pagamento, CommentCliente, CommentEmpresa
from datetime import date, timedelta, datetime
import datetime as dt

def only_digits(text):
    for i in text:
        try:
            int(i)
        except:
            return False
    return True
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
def valid_dates(weekdays):
    days_map = {1: 'seg',2:'ter',3:'qua',4:'qui',5:'sex',6:'sab',7:'dom'}
    CHOICES = []
    cont = 0
    while len(CHOICES) != 14:
        if weekdays[days_map[(date.today()+timedelta(days=cont)).isoweekday()]]:
            CHOICES.append((date.today()+timedelta(days=cont),'{0}/{1}'.format((date.today()+timedelta(days=cont)).day,(date.today()+timedelta(days=cont)).month)))
        cont += 1
    return CHOICES

def valid_hour(hora_inicio, hora_fim):
    return [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(hora_inicio.hour, hora_fim.hour+1)]

class ServicoForm(forms.ModelForm):
    data_agendada = forms.ChoiceField(widget=forms.RadioSelect)
    hora_agendada = forms.ChoiceField(choices=HOUR_CHOICES)
    endereco_agendado = forms.CharField(max_length=200)
    cliente = forms.ModelChoiceField(required=False,queryset=Cliente.objects.all())
    empresa = forms.ModelChoiceField(required=False,queryset=Empresa.objects.all())
    status = forms.CharField(required=False)
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows':'7','cols':'40','style':'resize:none'}))

    def __init__(self, weekdays,hora_inicio, hora_saida, *args, **kwargs):
        super(ServicoForm, self ).__init__(*args, **kwargs)
        self.fields['data_agendada'] = forms.ChoiceField(choices= valid_dates(weekdays), widget=forms.RadioSelect(attrs={'id':'dias-semana'}))
        self.fields['hora_agendada'] = forms.ChoiceField(choices=valid_hour(hora_inicio,hora_saida))
    
    class Meta:
        model = Servico
        fields = ('endereco_agendado','data_agendada','hora_agendada','cliente','empresa','status','desc')

class PagamentoForm(forms.ModelForm):
    valor_pagar = forms.DecimalField(max_digits=6,decimal_places=2, required=False)
    servico = forms.ModelChoiceField(required=False, queryset=Servico.objects.all())
    cliente = forms.ModelChoiceField(required=False,queryset=Cliente.objects.all())
    empresa = forms.ModelChoiceField(required=False,queryset=Empresa.objects.all())
    status = forms.CharField(required=False)
    titular = forms.CharField(max_length=50, required=False)
    cvv = forms.CharField(max_length=3, min_length=3, required=False)
    num_cartao = forms.CharField(max_length=12,min_length=12,required=False)
    validade = forms.DateField(required=False)
    
    def clean(self):
        cd = self.cleaned_data
        if not only_digits(cd.get('num_cartao')):
            self.add_error('num_cartao','Adicione um cartão válido')
        if not only_digits(cd.get('cvv')):
            self.add_error('cvv','Código de Segurança inválido')

    class Meta:
        model = Pagamento
        fields = ('valor_pagar', 'servico', 'cliente', 'empresa', 'status', 'titular', 'cvv', 'num_cartao', 'validade')

class CommentClienteForm(forms.ModelForm):
    author = forms.ModelChoiceField(required=False, queryset=Cliente.objects.all())
    empresa = forms.ModelChoiceField(required=False, queryset=Empresa.objects.all())
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':'7','cols':'40','style':'resize:none'}), required=False, max_length=300)
    rating = forms.DecimalField(required=False,max_value=5, min_value=0, max_digits=2, decimal_places=1)

    class Meta:
        model = CommentCliente
        fields = ('author', 'empresa','text','rating')

class CommentEmpresaForm(forms.ModelForm):
    author = forms.ModelChoiceField(required=False, queryset=Empresa.objects.all())
    cliente = forms.ModelChoiceField(required=False, queryset=Cliente.objects.all())
    text = forms.CharField(widget=forms.Textarea(attrs={'rows':'7','cols':'40','style':'resize:none'}), required=False, max_length=300)
    rating = forms.DecimalField(required=False,max_value=5, min_value=0, max_digits=2, decimal_places=1)

    class Meta:
        model = CommentCliente
        fields = ('author', 'cliente','text','rating')