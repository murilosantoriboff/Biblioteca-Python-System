from django.db import models
from datetime import date
from usuarios.models import Usuario
import datetime

class Categoria(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self) -> str:
        return self.nome

class Livros(models.Model):
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    co_autor = models.CharField(max_length=100, blank=True, null=True)
    data_cadastro = models.DateField(default=date.today)
    emprestado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Livro'

    def __str__(self) -> str:
        return self.nome

class Emprestimo(models.Model):
    choices_avaliacao = (
        ('P', 'Pessimo'),
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('M', 'Muito Bom'),
        ('O', 'Otimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank=True, null=True)
    nome_emprestado_anonimo = models.CharField(max_length=100, blank=True, null=True)
    data_emprestimo = models.DateTimeField(default=datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank=True, null=True)
    livro = models.ForeignKey(Livros, on_delete=models.DO_NOTHING)
    avaliacao = models.CharField(choices=choices_avaliacao, max_length=1, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.nome_emprestado} | {self.livro}'

