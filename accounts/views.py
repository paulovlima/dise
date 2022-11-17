from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from .forms import ClienteSignUpForm, EmpresaSignUpForm
from django.views import generic
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm(request)
    context = {"form":form}
    return render(request, "accounts/login_dise.html",context)
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')
    
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

class EmpresaSingUpView(generic.CreateView):
    model = User
    form_class = EmpresaSignUpForm
    template_name = 'accounts/singup_empresa.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'empresa'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
