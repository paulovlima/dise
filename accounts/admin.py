from django.contrib import admin
from .models import User, Cliente, Empresa, Tags
# Register your models here.

admin.site.register(User)
admin.site.register(Cliente)
admin.site.register(Empresa)
admin.site.register(Tags)