from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('perfil/<int:user_id>', views.perfil_view, name = 'perfil'),
    path('edit/<int:user_id>', views.edit_perfil_view, name= 'edit'),
    path('agendar/<int:user_id>', views.agendamento_view, name='agendar'),
    path('agendar/completo',views.agendamento_completo,name = 'agendamento_completo'),
    path('search/<str:tag_name>', views.tag_view, name='search_tag')
]