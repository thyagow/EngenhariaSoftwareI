from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^cadastro', views.cadastro_usuario, name='cadastro'),
	url(r'^login', views.login_usuario, name='login'),
	url(r'^logout', views.logout, name='logout'),
	url(r'^criar_produto', views.cadastro_produto, name='criar_produto'),
	url(r'^pesquisa', views.pesquisa, name='pesquisa'),
	url(r'^detalhe_produto', views.detalhe_produto, name='detalhe_produto'),
	url(r'^dar_lance', views.dar_lance, name='dar_lance'),
	url(r'^finalizar_venda', views.finalizar_venda, name='finalizar_venda'),
]
