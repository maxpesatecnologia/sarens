from django.db import models

class Solicitacao(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    assunto = models.CharField(max_length=150)
    mensagem = models.TextField()
    data_recebimento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.assunto}"
