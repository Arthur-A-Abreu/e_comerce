# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.index, name='index'),
    path('produto/<int:pk>/', views.detalhe_produto, name='detalhe_produto'),
]

