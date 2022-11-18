from django.shortcuts import render, get_object_or_404
from accounts.models import User
# Create your views here.

def index(request):
    user = request.user
    context = {'user':user}
    return render(request, 'agendamento/index.html', context)

def perfil_view(request, user_id):
    user = get_object_or_404(User, pk = user_id)
    context = {'user':user}
    return render(request, 'agendamento/perfil.html', context)