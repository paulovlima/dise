from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login
from django.shortcuts import redirect
from .forms import ClienteSignUpForm
from django.views import generic
from .models import User


class ClienteSingUpView(generic.CreateView):
    model = User
    form_class = ClienteSignUpForm
    template_name = 'accounts/singup_cliente.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'cliente'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
