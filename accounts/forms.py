from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Cliente, Empresa

class ClienteSignUpForm(UserCreationForm):
    cpf = forms.CharField(max_length=11,min_length=11)
    nome = forms.CharField(min_length=1)
    sobrenome = forms.CharField(min_length=1)
    tel = forms.CharField(min_length=10, max_length=11)
    nascimento = forms.DateField()
    email = forms.EmailField()
    image = forms.URLField()

    class Meta(UserCreationForm.Meta):
        model = User