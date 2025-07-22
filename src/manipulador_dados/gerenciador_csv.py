# src/manipulador_dados/gerenciador_csv.py

import csv
import os
from config.configuracoes import NOME_ARQUIVO_CSV, CSV_HEADERS, ESTADOS_DICT_INV

def inicializar_csv(caminho_arquivo=None):
    """
    Inicializa o arquivo CSV com os cabeçalhos.
    Cria o diretório 'data/processados' se não existir.
    """
    if caminho_arquivo is None:
        caminho_arquivo = os.path.join('data', 'processados', NOME_ARQUIVO_CSV)
    
    diretorio = os.path.dirname(caminho_arquivo)
    if not os.path.exists(diretorio):
        os.makedirs(diretorio)

    with open(caminho_arquivo, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSV_HEADERS)
    return caminho_arquivo

def adicionar_linha_csv(dados_linha, caminho_arquivo=None):
    """
    Adiciona uma linha de dados ao arquivo CSV.
    """
    if caminho_arquivo is None:
        caminho_arquivo = os.path.join('data', 'processados', NOME_ARQUIVO_CSV)

    with open(caminho_arquivo, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(dados_linha)

def carregar_dados_csv(caminho_arquivo=None):
    """
    Carrega os dados de um arquivo CSV e os retorna como uma lista de dicionários.
    """
    if caminho_arquivo is None:
        caminho_arquivo = os.path.join('data', 'processados', NOME_ARQUIVO_CSV)

    data = []
    try:
        with open(caminho_arquivo, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f'Erro: O arquivo {caminho_arquivo} não foi encontrado.')
        return None
    except Exception as e:
        print(f'Erro ao carregar CSV: {e}')
        return None
    
    if not data:
        print('Não há dados para analisar no CSV.')
        return None
    return data

def mapear_estado_para_string(estado_int):
    """Converte o valor inteiro do estado para sua representação em string."""
    return ESTADOS_DICT_INV.get(estado_int, "Desconhecido")