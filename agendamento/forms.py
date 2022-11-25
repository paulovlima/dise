from django import forms
from accounts.models import *
from .models import Servico, Pagamento, CommentCliente, CommentEmpresa
from datetime import date, timedelta, datetime
import datetime as dt

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
    desc = forms.CharField(widget=forms.Textarea(attrs={'rows':'5','cols':'40','style':'resize:none'}))

    def __init__(self, weekdays,hora_inicio, hora_saida, *args, **kwargs):
        super(ServicoForm, self ).__init__(*args, **kwargs)
        self.fields['data_agendada'] = forms.ChoiceField(choices= valid_dates(weekdays), widget=forms.RadioSelect(attrs={'id':'dias-semana'}))
        self.fields['hora_agendada'] = forms.ChoiceField(choices=valid_hour(hora_inicio,hora_saida))
    
    class Meta:
        model = Servico
        fields = ('endereco_agendado','data_agendada','hora_agendada','cliente','empresa','status','desc')