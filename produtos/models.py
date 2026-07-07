# pyrefly: ignore [missing-import]
from django.db import models

class Categoria(models.Model):
    nome = models.CharField('Nome', max_length=255)
    slug = models.SlugField('Slug', max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE, 
        related_name='produtos', 
        verbose_name='Categoria'
    )
    titulo = models.CharField('Título', max_length=255)
    descricao = models.TextField('Descrição')
    imagem = models.ImageField('Imagem', upload_to='produtos/')
    preco_original = models.DecimalField('Preço Original', max_digits=10, decimal_places=2)
    preco_promocional = models.DecimalField(
        'Preço Promocional', 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    frete_gratis = models.BooleanField('Frete Grátis', default=False)
    ativo = models.BooleanField('Ativo', default=True)
    
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.titulo

    @property
    def percentual_desconto(self):
        if self.preco_promocional and self.preco_original and self.preco_original > self.preco_promocional:
            desconto = ((self.preco_original - self.preco_promocional) / self.preco_original) * 100
            return int(round(desconto))
        return 0
