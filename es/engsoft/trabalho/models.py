from django.db import models

class Usuario(models.Model):
	nome = models.CharField(max_length=100)
	email = models.EmailField(max_length=100, unique=True)
	senha = models.CharField(max_length=100)
	saldo = models.FloatField(default = 0)
	def __str__(self):
		return self.nome + ", " + str(self.pk)



class Produto(models.Model):
	nome_produto = models.CharField(max_length=200)
	preco_inicial = models.FloatField()
	preco_final = models.FloatField(default=preco_inicial)
	data_inicio = models.DateTimeField(auto_now=True, auto_now_add=False)
	data_final = models.DateTimeField(auto_now=False, auto_now_add=False, default = None)
	estado = models.IntegerField(default=0)
	id_arrematante = models.IntegerField(default=None, null=True) #id do usuario que comprou
	comitente = models.ForeignKey('Usuario', on_delete=models.PROTECT)
	
	def __str__(self):
		return self.nome_produto

class Lance(models.Model):
	valor = models.FloatField()
	data = models.DateTimeField(auto_now=True, auto_now_add=False)
	usuario = models.ForeignKey('Usuario', on_delete=models.PROTECT)
	produto = models.ForeignKey('Produto', on_delete=models.PROTECT)
	def __str__(self):
		return str(self.valor) + ", " + str(self.data)
