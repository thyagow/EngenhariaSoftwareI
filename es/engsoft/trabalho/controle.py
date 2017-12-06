from .models import Usuario, Produto, Lance
from .daos import DaoUsuario, DaoProduto, DaoLance

class ControleUsuario():
	@staticmethod
	def existe(usuario):
		daoUsuario = DaoUsuario()
		usuarios = daoUsuario.getUsuarioByEmail(usuario.email)
		if usuarios == False:
			return False
		else:
			return True

	@staticmethod
	def verifica_login(usuario):
		daoUsuario = DaoUsuario()
		usuario2 = daoUsuario.getUsuarioByEmail(usuario.email)
		if usuario2 == False:
			return False
		if usuario2.senha != usuario.senha:
			return False
		return usuario2

	@staticmethod
	def cadastrar_usuario(usuario):
		daoUsuario = DaoUsuario()
		daoUsuario.cadastrarUsuario(usuario)
		return True



class ControleProduto():
	@staticmethod
	def cadastrar_produto(produto):
		daoProduto = DaoProduto()
		daoProduto.cadastrarProduto(produto)
		return True

	@staticmethod
	def getProduto(id_produto):
		daoProduto = DaoProduto()
		produto = daoProduto.getProduto(id_produto)
		return produto


	@staticmethod
	def pesquisa_nome(nome):
		daoProduto = DaoProduto()
		daoProduto.pesquisa
		produtos = Produto()
		produtos = Produto.objects.filter(nome_produto__contains=nome)
		return produtos

	@staticmethod
	def lista_todos():
		produtos = Produto()
		produtos = Produto.objects.all()
		return produtos

	@staticmethod
	def finalizar_venda():
		daoUsuario = DaoUsuario()
		daoProduto = DaoProduto()
		daoLance = DaoLance()
		maiorLance = Lance()
		produtos = Produto()
		produtos = daoProduto.pesquisaProdutoFimPrazo()
		for produto in produtos:
			maiorLance = daoLance.maiorLance(produto.pk)
			if maiorLance == False:
				daoProduto.cancelarProduto(produto.pk)
			else:
				daoProduto.venderProduto(produto.pk)
				usuario = maiorLance.arrematante
				usuario.saldo = usuario.saldo - maiorLance.valor * 0.8
				daoUsuario.atualizar_saldo(maiorLance.arrematante, maiorLance.valor)
		return True

	@staticmethod
	def finalizar_venda(id_produto):
		daoProduto = DaoProduto()
		daoUsuario = DaoUsuario()
		daoLance = DaoLance()
		produto = daoProduto.getProduto(id_produto)
		maiorLance = daoLance.maiorLance(produto.pk)
		if maiorLance == False:
			daoProduto.cancelarProduto(produto.pk)
		else:
			daoProduto.venderProduto(produto.pk)
			usuario = maiorLance.ausuario
			usuario.saldo = usuario.saldo - maiorLance.valor * 0.8
			daoUsuario.atualizar_saldo(maiorLance.usuario, maiorLance.valor)

class ControleLance():
	@staticmethod
	def criaLance(id_usuario, id_produto, valor):
		daoUsuario = DaoUsuario()
		daoProduto = DaoProduto()
		usuario = daoUsuario.getUsuario(id_usuario)
		produto = daoProduto.getProduto(id_produto)
		daoLance = DaoLance()
		lance = Lance()
		lance.produto = produto
		lance.usuario = usuario
		lance.valor = valor		
		if (produto.comitente.pk == id_usuario):
			return False
		if (valor * 0.2 > usuario.saldo):
			return False
		else:
			usuario.saldo = usuario.saldo - valor * 0.2
			daoUsuario.atualizarUsuario(usuario)
			maiorLance = daoLance.maiorLance(produto)
			if maiorLance != False:
				usuario2 = Usuario()
				usuario2 = maiorLance.usuario
				usuario2.saldo = usuario2.saldo + maiorLance.valor * 0.2
				daoUsuario.atualizarUsuario(usuario2)
			produto.preco_final = valor
			daoProduto.atualizarProduto(produto)
			daoLance.cadastrarLance(lance)
		return True
