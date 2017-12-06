from django.contrib import admin

from .models import Usuario, Produto, Lance

admin.site.register(Usuario)
admin.site.register(Produto)
admin.site.register(Lance)