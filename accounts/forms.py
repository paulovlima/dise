from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Cliente, Empresa

class ClienteSignUpForm(UserCreationForm):
    cpf = forms.CharField(max_length=11,min_length=11,required=True)
    nome = forms.CharField(required=True)
    sobrenome = forms.CharField(required=True)
    tel = forms.CharField(min_length=10, max_length=11,required=True)
    nascimento = forms.DateField(required=True)
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
        
