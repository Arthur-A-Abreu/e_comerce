# pyrefly: ignore [missing-import]
from django.shortcuts import render, get_object_or_404
# pyrefly: ignore [missing-import]
from django.db.models import Prefetch, Q
from .models import Categoria, Produto

def index(request):
    termo_pesquisa = request.GET.get('q', '').strip()
    
    if termo_pesquisa:
        # Se houver busca, exibimos apenas a lista de produtos correspondentes
        produtos = Produto.objects.filter(
            Q(titulo__icontains=termo_pesquisa) | Q(descricao__icontains=termo_pesquisa),
            ativo=True
        ).select_related('categoria')
        categorias = None
    else:
        # Se não houver busca, agrupamos por categoria, otimizando as queries (evita N+1)
        produtos = None
        categorias = Categoria.objects.prefetch_related(
            Prefetch(
                'produtos',
                queryset=Produto.objects.filter(ativo=True),
                to_attr='produtos_ativos'
            )
        )

    context = {
        'categorias': categorias,
        'produtos': produtos,
        'termo_pesquisa': termo_pesquisa,
        'busca_ativa': bool(termo_pesquisa),
    }
    return render(request, 'produtos/index.html', context)


def detalhe_produto(request, pk):
    # Garante que apenas produtos ativos sejam exibidos
    produto = get_object_or_404(Produto, pk=pk, ativo=True)
    
    # Busca produtos recomendados da mesma categoria (limite de 4, excluindo o atual)
    produtos_relacionados = Produto.objects.filter(
        categoria=produto.categoria,
        ativo=True
    ).exclude(pk=produto.pk)[:4]
    
    context = {
        'produto': produto,
        'produtos_relacionados': produtos_relacionados,
    }
    return render(request, 'produtos/detalhe.html', context)

