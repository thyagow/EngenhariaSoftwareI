from .models import Usuario, Produto, Lance
from datetime import date
from datetime import timedelta
from datetime import datetime
from django.db.models import Q
class DaoUsuario():
	@staticmethod
	def cadastrarUsuario(usuario): 
		usuario.save()
		return True

	@staticmethod
	def getUsuarioByEmail(email):
		try:
			usuario2 = Usuario.objects.get(email=email)
		except (KeyError, Usuario.DoesNotExist):
			return False
		return usuario2

	@staticmethod
	def atualizarUsuario(usuario):
		usuario.save()
		return True

	@staticmethod
	def getUsuario(id_usuario):
		usuario = Usuario()
		try:
			usuario = Usuario.objects.get(pk=id_usuario)
		except (KeyError, Usuario.DoesNotExist):
			return False
		return usuario

	def pesquisa(nome=None, email=None): # se nao precisar deleta
		query = Usuario.objects.all().order_by('nome')
		if nome != None:
			query.filter(nome__contains = nome)
		elif email != None:
			query.filter(email__contains = email)
		return query





class DaoProduto():
	@staticmethod
	def cadastrarProduto(produto): #deletar
		produto.save()
		return True

	@staticmethod
	def atualizarProduto(produto):
		produto.save()
		return True

	@staticmethod
	def getProduto(id_produto):
		produto = Produto()
		try:
			produto = Produto.objects.get(pk=id_produto)
		except (KeyError, Produto.DoesNotExist):
			return False
		return produto

	@staticmethod
	def pesquisaHistorico(id_usuario):
		query = Produto.objects.all()
		query = query.filter(Q(id_comprador=id_usuario) | Q(id_usuario=id_usuario))
		return query

	@staticmethod
	def cancelarProduto(idproduto):
		produto = Produto()
		try:
			produto = Produto.objects.get(pk=idproduto, estado=0)
		except (KeyError, Produto.DoesNotExist):
			return False
		produto.estado = 2 # cancelado
		produto.save()
		return True

	@staticmethod
	def venderProduto(idproduto):
		produto = Produto()
		try:
			produto = Produto.objects.get(pk=idproduto, estado=0)# a venda
		except (KeyError, Produto.DoesNotExist):
			return False
		try:
			lance = Lance.objects.filter(pk=idproduto).order_by('valor').desc()[0]
		except (KeyError, Lance.DoesNotExist):
			return False
		produto.id_comprador = lance.usuario.pk
		produto.estado = 1 # vendido
		produto.save()
		return True

	@staticmethod
	def pesquisa(nome=None, dataini=None, datafim=None, precomin=None, precomax=None, estado=None, offset=0, limit=None, order='data_inicio'):
		query = Produto.objects.all()
		if nome != None:
			query = query.filter(nome_produto__contains = nome)
		elif dataini != None:
			query = query.filter(data_inicio__gte = dataini) # lixo
		elif datafim != None:
			query = query.filter(data_final__lte = datafim)
		elif precomin != None:
			query = query.filter(preco_final__gte = precomin)
		elif precomax != None:
			query = query.filter(preco_final__lte = precomax)
		elif estado != None:
			query = query.filter(estado = estado)
		if limit == None:
			query.order_by(order)[offset:]
		else:
			query.order_by(order)[offset:limit]
		return query

	def pesquisaProdutoFimPrazo(clock):
		data = datetime.today()- timedelta(minutes=clock)
		try:
			query = Produto.objects.filter(data_final__gte = data)
		except IndexError:
			return False
		return query


class DaoLance():
	@staticmethod
	def cadastrarLance(lance):
		lance.save();
		return True;

	@staticmethod
	def pesquisa(id_usuario=None, id_produto=None, offset=0, limit=None):
		try:
			query = Lance.objects.all
			if id_usuario != None:
				query.filter(id_usuario=id_usuario)
			elif id_produto != None:
				query.filter(id_produto=id_produto)
			if limit == None:
				query.order_by('-valor')[offset:]
			else:
				query.order_by('-valor')[0]
			return query
		except (KeyError, Lance.DoesNotExist):
			return False

	@staticmethod
	def maiorLance(produto):
		try:
			query = Lance.objects.filter(produto=produto).order_by('-valor')[0]
		except IndexError:
			return False
		return query