from django.urls import path

from . import views

urlpatterns = [
    path('singup_cliente',views.ClienteSingUpView.as_view(),name='singup_cliente'),
    path('singup_empresa',views.EmpresaSingUpView.as_view(),name='singup_empresa')
]