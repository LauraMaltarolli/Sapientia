from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    data_nascimento = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Data de Nascimento"
    )
    
    # Adicionamos os campos ManyToManyField com related_name para resolver o conflito
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_set",
        related_query_name="usuario",
    )


class Dilema(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Dilema"
        verbose_name_plural = "Dilemas"

    def __str__(self):
        return self.titulo

class SessaoReflexao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    dilema = models.ForeignKey(Dilema, on_delete=models.CASCADE, verbose_name="Dilema")
    data_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Início da Sessão")

    class Meta:
        verbose_name = "Sessão de Reflexão"
        verbose_name_plural = "Sessões de Reflexão"

    def __str__(self):
        return f"Sessão de {self.usuario} sobre '{self.dilema.titulo}'"

class Mensagem(models.Model):
    class Remetente(models.TextChoices):
        USUARIO = 'USUARIO', 'Usuário'
        IA = 'IA', 'IA'

    sessao = models.ForeignKey(
        SessaoReflexao,
        on_delete=models.CASCADE,
        related_name='mensagens',
        verbose_name="Sessão"
    )
    remetente = models.CharField(max_length=7, choices=Remetente.choices, verbose_name="Remetente")
    conteudo = models.TextField(verbose_name="Conteúdo")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Mensagem"
        verbose_name_plural = "Mensagens"
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.get_remetente_display()} em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

class TesteFilosofico(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título do Teste")
    perguntas = models.JSONField(verbose_name="Perguntas e Opções")

    class Meta:
        verbose_name = "Teste Filosófico"
        verbose_name_plural = "Testes Filosóficos"

    def __str__(self):
        return self.titulo

class ResultadoTeste(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    teste = models.ForeignKey(TesteFilosofico, on_delete=models.CASCADE, verbose_name="Teste")
    resultado = models.CharField(max_length=150, verbose_name="Resultado")
    data_realizacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Realização")

    class Meta:
        verbose_name = "Resultado de Teste"
        verbose_name_plural = "Resultados de Testes"

    def __str__(self):
        return f"Resultado de {self.usuario} para '{self.teste.titulo}'"

class TeoriaFilosofica(models.Model):
    nome_teoria = models.CharField(max_length=150, verbose_name="Nome da Teoria")
    descricao = models.TextField(verbose_name="Descrição")
    principais_pensadores = models.CharField(max_length=255, verbose_name="Principais Pensadores")

    class Meta:
        verbose_name = "Teoria Filosófica"
        verbose_name_plural = "Teorias Filosóficas"

    def __str__(self):
        return self.nome_teoria

class DilemaCriado(models.Model):
    usuario_criador = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário Criador")
    protagonista = models.CharField(max_length=100, verbose_name="Protagonista")
    objetivo = models.TextField(verbose_name="Objetivo")
    conflito = models.TextField(verbose_name="Conflito")
    opcao1 = models.CharField(max_length=255, verbose_name="Opção 1")
    opcao2 = models.CharField(max_length=255, verbose_name="Opção 2")
    solucao_do_criador = models.CharField(max_length=255, verbose_name="Solução do Criador")
    justificativa_do_criador = models.TextField(verbose_name="Justificativa do Criador")

    class Meta:
        verbose_name = "Dilema Criado por Usuário"
        verbose_name_plural = "Dilemas Criados por Usuários"

    def __str__(self):
        return f"Dilema criado por {self.usuario_criador}"

class MensagemDilemaCriado(models.Model):
    class Remetente(models.TextChoices):
        USUARIO = 'USUARIO', 'Usuário'
        IA = 'IA', 'IA'

    dilema_criado = models.ForeignKey(
        DilemaCriado,
        on_delete=models.CASCADE,
        related_name='mensagens',
        verbose_name="Dilema Criado"
    )
    remetente = models.CharField(max_length=7, choices=Remetente.choices, verbose_name="Remetente")
    conteudo = models.TextField(verbose_name="Conteúdo")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    class Meta:
        verbose_name = "Mensagem de Dilema Criado"
        verbose_name_plural = "Mensagens de Dilemas Criados"
        ordering = ['timestamp']

    def __str__(self):
        return f"Mensagem em '{self.dilema_criado.protagonista}' às {self.timestamp.strftime('%H:%M')}"

class Filosofo(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Nome")
    imagem_url = models.URLField(max_length=255, verbose_name="URL da Imagem")
    periodo_historico = models.CharField(max_length=100, verbose_name="Período Histórico")
    citacao_destaque = models.TextField(verbose_name="Citação em Destaque")

    class Meta:
        verbose_name = "Filósofo"
        verbose_name_plural = "Filósofos"

    def __str__(self):
        return self.nome

class AcaoAnalisada(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuário")
    descricao_acao_inicial = models.CharField(max_length=255, verbose_name="Descrição da Ação")
    respostas_do_usuario = models.JSONField(verbose_name="Respostas do Usuário")
    data_analise = models.DateTimeField(auto_now_add=True, verbose_name="Data da Análise")

    class Meta:
        verbose_name = "Ação Analisada"
        verbose_name_plural = "Ações Analisadas"

    def __str__(self):
        return f"Análise de '{self.descricao_acao_inicial}' para {self.usuario}"