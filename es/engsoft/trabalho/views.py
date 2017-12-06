from django.shortcuts import render
from django.template import loader
from datetime import date
from datetime import timedelta

from django.http import HttpResponse
from .models import Usuario, Produto 
from .controle import ControleUsuario, ControleProduto, ControleLance

# Usuario -----------------------------------------------------------------------------

def index(request):
	if 'nome' in request.session:
		usuario = Usuario.objects.get(email=request.session['email'])
		request.session['id'] = usuario.pk
		request.session['nome'] = usuario.nome
		request.session['email'] = usuario.email
		request.session['saldo'] = usuario.saldo
		return render(request, 'trabalho/indexlogado.html', {'usuario': usuario})
	else:
		return render(request, 'trabalho/index.html', None)

def cadastro_usuario(request):
	if request.method == "POST":
		cUsuario = ControleUsuario()
		usuario = Usuario()
		usuario.nome = request.POST['nome']
		usuario.email = request.POST['email']
		usuario.senha = request.POST['senha']
		usuario.saldo = 0;
		existe = cUsuario.existe(usuario)
		if existe:
			return render(request, 'trabalho/errado.html', None)
		else:
			cUsuario.cadastrar_usuario(usuario)
			return render(request, 'trabalho/voltar.html', {'usuario': usuario})
	else: 
		return render(request, 'trabalho/cadastro.html', None)
	
def login_usuario(request):
	if request.method == "POST":
		cUsuario = ControleUsuario()
		usuario = Usuario()
		usuario.email = request.POST['email']
		usuario.senha = request.POST['senha']
		usuario2 = cUsuario.verifica_login(usuario)
		if usuario2 == False:
			return render(request, 'trabalho/errado.html',None )
		else:
			request.session['id'] = usuario2.pk
			request.session['nome'] = usuario2.nome
			request.session['email'] = usuario2.email
			request.session['saldo'] = usuario2.saldo
			return render(request, 'trabalho/voltar.html', {'usuario': usuario})
	else: 
		return render(request, 'trabalho/login.html', None)

def logout(request):
	if 'nome' in request.session:
		del request.session['id']
		del request.session['nome']
		del request.session['email']
		del request.session['saldo']
	return render(request, 'trabalho/index.html', None)

# Produto ----------------------------------------------------------------------------

def cadastro_produto(request):
	if request.method == "POST":
		cProduto = ControleProduto()
		produto = Produto()
		produto.nome_produto = request.POST['nome']
		produto.preco_inicial = request.POST['p_inicial']
		produto.preco_final = produto.preco_inicial
		produto.data_inicial = date.today()
		produto.data_final = date.today() + timedelta(days=int(request.POST['duracao']))
		produto.comitente = Usuario.objects.get(pk=request.session['id'])
		cProduto.cadastrar_produto(produto)
		return render(request, 'trabalho/voltar.html', None)
	else: 
		return render(request, 'trabalho/criar_produto.html', {'lista': [1, 3, 7, 15, 30]})

def pesquisa(request):
	if request.method == "POST":
		cProduto = ControleProduto()
		nome = request.POST['nome']
		produtos = cProduto.pesquisa_nome(nome)
		pesquisa = "Listando produtos com o atributo nome = '" + nome + "'"
		id_usuario = request.session['id']
		return render(request, 'trabalho/lista_produto.html', {'produtos': produtos, 'pesquisa': pesquisa, 'id_usuario':id_usuario})
	else:
		return render(request, 'trabalho/erro404.html',None)

def detalhe_produto(request):
	return render(request, 'trabalho/index.html', None)

def dar_lance(request):
	if 'id' in request.GET:
		usuario = Usuario.objects.get(email=request.session['email'])
		cProduto = ControleProduto()
		produto = Produto()
		id_produto = request.GET['id']
		produto = cProduto.getProduto(id_produto)
		produto.preco_final = produto.preco_final+1
		if produto == False:
			return render(request, 'trabalho/erro404.html',None)
		else:
			return render(request, 'trabalho/lance.html', {'produto': produto, 'usuario':usuario})
	elif request.method == "POST":
		id_produto = request.POST['id_produto']
		id_usuario = request.session['id']
		valor = request.POST['valor_lance']
		cLance = ControleLance()
		result = cLance.criaLance(id_usuario, id_produto, float(valor))
		if result:
			return render(request, 'trabalho/voltar.html')
		return render(request, 'trabalho/erro404.html',None)
	else:
		return render(request, 'trabalho/erro404.html',None)

def finalizar_venda(request):
	return render(request, 'trabalho/erro404.html', None)

