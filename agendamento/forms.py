from django import forms
from accounts.models import *
from .models import Servico, Pagamento, CommentCliente, CommentEmpresa
from datetime import date, timedelta
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

class ServicoForm(forms.ModelForm):
    data_agendada = forms.ChoiceField(widget=forms.RadioSelect)
    hora_agendada = forms.ChoiceField(choices=HOUR_CHOICES)
    cliente = forms.ModelChoiceField(required=False,queryset=Cliente.objects.all())
    empresa = forms.ModelChoiceField(required=False,queryset=Empresa.objects.all())
    orcamento = forms.DecimalField(min_value=0,max_digits=6,decimal_places=2)
    status = forms.CharField()
    desc = forms.CharField()
    def __init__(self, weekdays, *args, **kwargs):
        super(ServicoForm, self ).__init__(*args, **kwargs)
        self.fields['data_agendada'] = forms.ChoiceField(choices= valid_dates(weekdays), widget=forms.RadioSelect(attrs={'id':'dias-semana'}))
        
    class Meta:
        model = Servico
        fields = ('data_agendada','hora_agendada','cliente','empresa','orcamento','status','desc')