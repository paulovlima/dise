from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('singup_cliente',views.ClienteSingUpView.as_view(),name='singup_cliente'),
    path('singup_empresa',views.EmpresaSingUpView.as_view(),name='singup_empresa'),
    path('login_dise',views.login_view,name = 'login_dise'),
    path('logout',views.logout_view,name='logout')
]