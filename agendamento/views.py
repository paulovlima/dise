from django.shortcuts import render, get_object_or_404
from accounts.models import User, Tags, Empresa
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.forms import EmpresaUpdate, ClienteUpdate
from django.views import generic
# Create your views here.

def index(request):
    user = request.user
    empresa_list = Empresa.objects.all()
    context = {'user':user, "empresa_list":empresa_list}
    return render(request, 'agendamento/index.html', context)

def perfil_view(request, user_id):
    perfil = get_object_or_404(User, pk = user_id)
    context = {'perfil':perfil}
    return render(request, 'agendamento/perfil.html', context)

@login_required
def edit_perfil_view(request, user_id):
    perfil = get_object_or_404(User, pk = user_id)
    user = request.user
    if perfil.id != user.id:
        return HttpResponseRedirect(
            reverse('index')
        )
    else:
        if request.method == 'POST':
            if perfil.is_empresa:
                empresa = perfil.empresa
                form = EmpresaUpdate(request.POST)
                if form.is_valid():
                    empresa.tags.set(form.cleaned_data.get('tags'))
                    empresa.tel = form.cleaned_data.get('tel')
                    empresa.email = form.cleaned_data.get('email')
                    empresa.horario_inicio = form.cleaned_data.get('horario_inicio')
                    empresa.horario_fim = form.cleaned_data.get('horario_fim')
                    empresa.image = form.cleaned_data.get('image')
                    empresa.seg = form.cleaned_data.get('seg')
                    empresa.ter = form.cleaned_data.get('ter')
                    empresa.qua = form.cleaned_data.get('qua')
                    empresa.qui = form.cleaned_data.get('qui')
                    empresa.sex = form.cleaned_data.get('sex')
                    empresa.sab = form.cleaned_data.get('sab')
                    empresa.dom = form.cleaned_data.get('dom')
                    empresa.desc = form.cleaned_data.get('desc')
                    empresa.save()
                    return HttpResponseRedirect(
                        reverse('perfil', args=(perfil.pk,))
                        )
            elif perfil.is_cliente:
                cliente = perfil.cliente
                form = ClienteUpdate(request.POST)
                if form.is_valid():
                    cliente.tel = form.cleaned_data.get('tel')
                    cliente.email = form.cleaned_data.get('email')
                    cliente.image = form.cleaned_data.get('image')
                    cliente.save()
                    return HttpResponseRedirect(
                        reverse('perfil', args=(perfil.pk,))
                        )
        else:
            if perfil.is_empresa:
                empresa = perfil.empresa
                form = EmpresaUpdate(
                    initial={
                        'tags':[
                            tag for tag in empresa.tags.all().values_list("id", flat=True)
                        ],
                        'tel':empresa.tel,
                        'endereco':empresa.endereco,
                        'image':empresa.image,
                        'horario_inicio':empresa.horario_inicio,
                        'horario_fim': empresa.horario_fim,
                        'email': empresa.email,
                        'seg': empresa.seg,
                        'ter': empresa.ter,
                        'qua': empresa.qua,
                        'qui': empresa.qui,
                        'sex': empresa.sex,
                        'sab': empresa.sab,
                        'dom': empresa.dom,
                        'desc': empresa.desc
                    }
                )
            elif perfil.is_cliente:
                cliente = perfil.cliente
                form = ClienteUpdate(
                    initial={
                        'tel': cliente.tel,
                        'email': cliente.email,
                        'image': cliente.image
                    }
                )
        context = {'perfil':perfil, 'form': form}
        return render(request, 'agendamento/edit.html', context)

def agendamento_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if user.is_cliente:
        return HttpResponseRedirect(
            reverse('index')
        )
    empresa = user.empresa
    context = {'empresa': empresa}
    return render(request, 'agendamento/agendar.html', context)