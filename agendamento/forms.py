from django import forms
from .models import Servico, Pagamento, CommentCliente, CommentEmpresa
from datetime import date, timedelta
import datetime as dt

HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
def valid_dates(weekdays):
    days_map = {1: 'seg',2:'ter',3:'qua',4:'qui',5:'sex',6:'sab',7:'dom'}
    CHOICES = []
    cont = 0
    while len(CHOICES) != 14:
        if weekdays[days_map[date.today().isoweekday()]]:
            CHOICES.append(('{0}/{1}'.format((date.today()+timedelta(days=cont)).day,(date.today()+timedelta(days=cont)).month),date.today()+timedelta(days=cont)))
            cont += 1
    return CHOICES

class ServicoForm(forms.ModelForm):
    def __init__(self, weekdays):
        pass