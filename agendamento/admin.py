from django.contrib import admin

# Register your models here.
from .models import Servico, Pagamento, CommentCliente, CommentEmpresa

admin.site.register(Servico)
admin.site.register(Pagamento)
admin.site.register(CommentCliente)
admin.site.register(CommentEmpresa)
