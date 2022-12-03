from django.shortcuts import render, get_object_or_404
from accounts.models import User, Tags, Empresa
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from accounts.forms import EmpresaUpdate, ClienteUpdate
from .forms import ServicoForm, PagamentoForm, CommentClienteForm, CommentEmpresaForm
from .models import Servico, Pagamento, CommentCliente, CommentEmpresa
from datetime import date
from django.db.models import Q, Avg
# Create your views here.

def lista_empresa(empresa_list, filtro = ''):
    if filtro == '':
        todas = Empresa.objects.all()
        for empresa in todas:
            if empresa in empresa_list:
                continue
            empresa_list.append(empresa)
    else:
        todas = Empresa.objects.filter(nome_fantasia__icontains=filtro)
        for empresa in todas:
            if empresa in empresa_list:
                continue
            empresa_list.append(empresa)
    return empresa_list


def index(request):
    user = request.user
    tags = Tags.objects.all()
    empresa_list = []
    if request.GET.get('query',False):
        search_term = request.GET['query'].lower()
        if search_term != '':
            empresa_list = Empresa.objects.filter(nome_fantasia__icontains=search_term)
    else:
        for empresa in CommentCliente.objects.values('empresa').annotate(Avg('rating')).order_by('-rating__avg'):
            empresa_list.append(User.objects.filter(pk=empresa['empresa'])[0].empresa)
        empresa_list = lista_empresa(empresa_list)
    context = {'user':user, "empresa_list":empresa_list,'tags':tags}
    return render(request, 'agendamento/index.html', context)

def perfil_view(request, user_id):
    perfil = get_object_or_404(User, pk = user_id)
    if perfil.is_cliente:
        comments = CommentEmpresa.objects.filter(cliente = perfil.cliente)
        rating = comments.aggregate(Avg('rating'))['rating__avg']
        if rating == None:
            rating = 5
    else:
        comments = CommentCliente.objects.filter(empresa = perfil.empresa)
        rating = comments.aggregate(Avg('rating'))['rating__avg']
        if rating == None:
            rating = 5
    context = {'perfil':perfil, 'comments': comments,'rating':rating}
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
    perfil = get_object_or_404(User, pk=user_id)
    user = request.user
    rating = CommentCliente.objects.filter(empresa = perfil.empresa).aggregate(Avg('rating'))['rating__avg']
    if rating == None:
            rating = 5
    if perfil.is_cliente:
        return HttpResponseRedirect(
        reverse('index'))
    
    empresa = perfil.empresa
    weekday = {'seg':empresa.seg,
                'ter': empresa.ter,
                'qua': empresa.qua,
                'qui': empresa.qui,
                'sex': empresa.sex,
                'sab': empresa.sab,
                'dom': empresa.dom
    }
    form = ServicoForm(weekdays= weekday, hora_inicio=empresa.horario_inicio, hora_saida= empresa.horario_fim)
    if request.method == 'POST':
        form = ServicoForm(weekday, empresa.horario_inicio, empresa.horario_fim, request.POST)
        if form.is_valid():
            servico = Servico(
                cliente = request.user.cliente,
                empresa = empresa,
                hora_agendada = form.cleaned_data.get('hora_agendada'),
                data_agendada = form.cleaned_data.get('data_agendada'),
                endereco_agendado = form.cleaned_data.get('endereco_agendado'),
                status = 'ESPERANDO',
                desc = form.cleaned_data.get('desc'),
            )
            servico.save()
            return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    context = {'empresa': empresa, 'form': form, 'rating': rating}
    return render(request, 'agendamento/agendar.html', context)

def tag_view(request, tag_name):
    tag = get_object_or_404(Tags, name=tag_name)
    tags = Tags.objects.all()
    if request.GET.get('query',False):
        search_term = request.GET['query'].lower()
        if search_term != '':
            empresa_list = tag.empresa_set.filter(nome_fantasia__icontains=search_term)
    else:
        empresa_list = tag.empresa_set.all()    
    context = {"empresa_list":empresa_list,'tag':tag, 'tags':tags}
    return render(request, 'agendamento/tags.html', context)

def servico_view(request, user_id):
    user = request.user
    perfil = get_object_or_404(User, pk=user_id)
    if request.GET.get('cancel',False):
        cancelado =request.GET['cancel']
        serv_cancelado = get_object_or_404(Servico,pk=cancelado)
        serv_cancelado.status = 'CANCELADO'
        serv_cancelado.save()
    if request.GET.get('cancelPagamento',False):
        cancelado =request.GET['cancelPagamento']
        pag_cancelado = get_object_or_404(Pagamento,pk=cancelado)
        pag_cancelado.status = 'CANCELADO'
        pag_cancelado.save()
    if request.GET.get('cancelAgendado',False):
        cancelado =request.GET['cancelAgendado']
        pag_cancelado = get_object_or_404(Pagamento,pk=cancelado)
        pag_cancelado.status = 'CANCELADO'
        pag_cancelado.save()
    if perfil.id != user.id:
        return HttpResponseRedirect(
            reverse('index')
        )
    if perfil.is_cliente:
        cliente = perfil.cliente
        servicos = Servico.objects.filter(cliente = cliente,status = 'ESPERANDO')
        pagamento = Pagamento.objects.filter(cliente = cliente,status = 'ESPERANDO')
        pagos = Pagamento.objects.filter(Q(status = 'PAGO') | Q(status = 'COMENTADO_EMPRESA'),cliente= cliente)

    else:
        empresa = perfil.empresa
        servicos = Servico.objects.filter(empresa= empresa, status = 'ESPERANDO')
        pagamento = Pagamento.objects.filter(empresa= empresa, status = 'ESPERANDO')
        pagos = Pagamento.objects.filter(Q(status = 'PAGO') | Q(status = 'COMENTADO_CLIENTE'),empresa= empresa)

    context = {'servicos': servicos, 'perfil':perfil, 'pagamento':pagamento, 'pagos':pagos}
    return render(request,'agendamento/agend_list.html', context)

def orcamento_view(request, servico_id):
    user = request.user
    servico = get_object_or_404(Servico, pk = servico_id)
    if user.is_cliente or user.id != servico.empresa.user.id:
        return HttpResponseRedirect(
            reverse('perfil', args=(user.id,))
        )
    form = PagamentoForm()
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento = Pagamento(
                valor_pagar = form.cleaned_data.get('valor_pagar'),
                cliente = servico.cliente,
                empresa = servico.empresa,
                servico = servico,
                status = 'ESPERANDO',
                num_cartao = '',
                titular = '',
                cvv = '',
                validade = date.today()
            )
            servico.status = 'PAGAMENTO'
            servico.save()
            pagamento.save()
            return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    context = {'servico':servico, 'form': form}
    return render(request,'agendamento/orcamento.html',context)

def pagamento_view(request, pag_id):
    user = request.user
    pagamento = get_object_or_404(Pagamento, pk = pag_id)
    if user.is_empresa or user.id != pagamento.cliente.user.id:
        return HttpResponseRedirect(
            reverse('perfil', args=(user.id,))
        )
    form = PagamentoForm()
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagamento.titular = form.cleaned_data.get('titular')
            pagamento.cvv = form.cleaned_data.get('cvv')
            pagamento.num_cartao = form.cleaned_data.get('num_cartao')
            mes = int(request.POST['mes'])
            ano = int(request.POST['ano'])
            pagamento.validade = date(year=ano, month= mes, day=1)
            pagamento.status = 'PAGO'
            servico = pagamento.servico
            servico.status = 'AGENDADO'
            pagamento.save()
            servico.save()
            return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    context = {'pagamento':pagamento, 'form':form}
    return render(request, 'agendamento/pagar.html', context)

def comentario_view(request,pag_id):
    user =request.user
    pagamento = get_object_or_404(Pagamento, Q(status='PAGO') | Q(status='COMENTADO_CLIENTE') | Q(status ='COMENTADO_EMPRESA'), pk = pag_id)
    if (user.id != pagamento.cliente.user.id and user.is_cliente) or (user.id != pagamento.empresa.user.id and user.is_empresa):
        return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    elif user.is_cliente and (pagamento.status == 'COMENTADO_CLIENTE' or pagamento.status == 'COMENTADO_CLIENTE_EMPRESA'):
        return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    elif user.is_empresa and (pagamento.status == 'COMENTADO_EMPRESA' or pagamento.status == 'COMENTADO_CLIENTE_EMPRESA'):
        return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    if user.is_cliente:
        form = CommentClienteForm(
            initial= {
                'text': '',
                'rating': 0
            }
        )
        if request.method == 'POST':
            form = CommentClienteForm(request.POST)
            if form.is_valid():
                comment = CommentCliente(
                    author = pagamento.cliente.user,
                    empresa = pagamento.empresa,
                    text = form.cleaned_data.get('text'),
                    rating = form.cleaned_data.get('rating')
                )
                if pagamento.status == 'PAGO':
                    pagamento.status = 'COMENTADO_CLIENTE'
                    pagamento.save()
                elif pagamento.status == 'COMENTADO_EMPRESA':
                    pagamento.status = 'COMENTADO_CLIENTE_EMPRESA'
                    pagamento.save()
                if not form.cleaned_data.get('text') == '' and not form.cleaned_data.get('rating') == 0:
                    comment.save()
            return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    else:
        form = CommentEmpresaForm(
            initial= {
                'text': '',
                'rating': 0
            }
        )
        if request.method == 'POST':
            form = CommentEmpresaForm(request.POST)
            if form.is_valid():
                comment = CommentEmpresa(
                    author = pagamento.empresa.user,
                    cliente = pagamento.cliente,
                    text = form.cleaned_data.get('text'),
                    rating = form.cleaned_data.get('rating')
                )
                if pagamento.status == 'PAGO':
                    pagamento.status = 'COMENTADO_EMPRESA'
                    pagamento.save()
                elif pagamento.status == 'COMENTADO_CLIENTE':
                    pagamento.status = 'COMENTADO_CLIENTE_EMPRESA'
                    pagamento.save()
                if not form.cleaned_data.get('text') == '' and not form.cleaned_data.get('rating') == 0:
                    comment.save()
            return HttpResponseRedirect(
        reverse('lista_servicos', args=(user.id,)))
    context = {'pagamento': pagamento, 'form':form}
    return render(request, 'agendamento/comentario.html',context)