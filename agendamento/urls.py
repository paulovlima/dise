from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/<int:user_id>', views.perfil_view, name = 'perfil'),
    path('edit/<int:user_id>', views.edit_perfil_view, name= 'edit'),
    path('agendar/<int:user_id>', views.agendamento_view, name='agendar'),
    path('agendar/completo',views.agendamento_completo,name = 'agendamento_completo'),
    path('search/<str:tag_name>', views.tag_view, name='search_tag'),
    path('perfil/lista_servicos/<int:user_id>', views.servico_view, name = 'lista_servicos'),
    path('agendar/orcamento/<int:servico_id>',views.orcamento_view, name= 'criar_orcamento'),
    path('agendar/pagar/<int:pag_id>', views.pagamento_view, name='pagar'),
    
]