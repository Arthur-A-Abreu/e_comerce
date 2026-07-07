# pyrefly: ignore [missing-import]
from django.contrib import admin
# pyrefly: ignore [missing-import]
from django.utils.safestring import mark_safe
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        'exibir_imagem',
        'titulo', 
        'categoria', 
        'preco_original', 
        'preco_promocional', 
        'frete_gratis', 
        'ativo', 
        'criado_em'
    )
    list_filter = ('ativo', 'frete_gratis', 'categoria', 'criado_em')
    search_fields = ('titulo', 'descricao')
    list_editable = ('preco_original', 'preco_promocional', 'frete_gratis', 'ativo')
    readonly_fields = ('exibir_imagem_detalhe', 'criado_em', 'atualizado_em')
    
    # Custom display of product image in the list view
    def exibir_imagem(self, obj):
        if obj.imagem:
            return mark_safe(f'<img src="{obj.imagem.url}" width="50" height="50" style="object-fit: cover; border-radius: 4px;" />')
        return "Sem imagem"
    
    exibir_imagem.short_description = 'Miniatura'

    # Custom display of product image in the detail view
    def exibir_imagem_detalhe(self, obj):
        if obj.imagem:
            return mark_safe(f'<img src="{obj.imagem.url}" max-width="300" style="max-height: 300px; border-radius: 8px;" />')
        return "Sem imagem"
    
    exibir_imagem_detalhe.short_description = 'Visualização da Imagem'
