# src/visualizacao/gerador_graficos.py

import matplotlib.pyplot as plt # Manter por enquanto se ainda for usar para outros fins
import seaborn as sns          # Manter por enquanto se ainda for usar para outros fins
import pandas as pd
import os
import plotly.graph_objects as go # Importar Plotly
from plotly.subplots import make_subplots # Importar para múltiplos gráficos se necessário
import plotly.express as px # Para gráficos mais simples

from config.configuracoes import ESTADOS_DICT # Manter ESTADOS_DICT

# from config.configuracoes import (
#     LIMIAR_ANGULO_JOELHO_EM_PE,
#     LIMIAR_ANGULO_JOELHO_AGACHADO,
#     LIMIAR_QUEDA_Y_PX_PERCENTUAL,
#     ESTADOS_DICT # Adicionar ESTADOS_DICT
# )

def _garantir_diretorio_relatorios_existe():
    """Cria o diretório de relatórios se não existir."""
    diretorio_relatorios = os.path.join('data', 'relatorios')
    if not os.path.exists(diretorio_relatorios):
        os.makedirs(diretorio_relatorios)
    return diretorio_relatorios

def gerar_grafico_angulos(dados_csv, fps, limiar_joelho_em_pe, limiar_joelho_agachado, nome_arquivo="angulos_agachamento.html"): # Novos parâmetros
    """
    Gera e salva um gráfico interativo (Plotly) de série temporal dos ângulos dos joelhos e tornozelos.
    """
    if dados_csv is None:
        print("Dados CSV não disponíveis para gerar o gráfico de ângulos.")
        return None

    df = pd.DataFrame(dados_csv)
    df['Angulo_Joelho_Esquerdo'] = pd.to_numeric(df['Angulo_Joelho_Esquerdo'], errors='coerce')
    df['Angulo_Joelho_Direito'] = pd.to_numeric(df['Angulo_Joelho_Direito'], errors='coerce')
    df['Angulo_Tornozelo_Esquerdo'] = pd.to_numeric(df['Angulo_Tornozelo_Esquerdo'], errors='coerce')
    df['Angulo_Tornozelo_Direito'] = pd.to_numeric(df['Angulo_Tornozelo_Direito'], errors='coerce')
    df['Frame'] = pd.to_numeric(df['Frame'], errors='coerce')
    df['Tempo_Segundos'] = df['Frame'] / fps

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['Tempo_Segundos'], y=df['Angulo_Joelho_Esquerdo'], mode='lines', name='Joel. Esq.', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Tempo_Segundos'], y=df['Angulo_Joelho_Direito'], mode='lines', name='Joel. Dir.', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=df['Tempo_Segundos'], y=df['Angulo_Tornozelo_Esquerdo'], mode='lines', name='Tornoz. Esq.', line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Tempo_Segundos'], y=df['Angulo_Tornozelo_Direito'], mode='lines', name='Tornoz. Dir.', line=dict(color='purple', dash='dash')))
    
    # Usar os novos parâmetros de limiar
    fig.add_hline(y=limiar_joelho_em_pe, line_dash="dot", line_color="gray", annotation_text=f'Limiar Joelho Em Pé ({limiar_joelho_em_pe}°)', annotation_position="top right")
    fig.add_hline(y=limiar_joelho_agachado, line_dash="dash", line_color="gray", annotation_text=f'Limiar Joelho Agachado ({limiar_joelho_agachado}°)', annotation_position="bottom right")

    fig.update_layout(
        title='Variação dos Ângulos dos Joelhos e Tornozelos ao Longo do Tempo',
        xaxis_title='Tempo (segundos)',
        yaxis_title='Ângulo (graus)',
        hovermode="x unified",
        height=500
    )
    
    diretorio_relatorios = _garantir_diretorio_relatorios_existe()
    caminho_completo_arquivo = os.path.join(diretorio_relatorios, nome_arquivo)
    fig.write_html(caminho_completo_arquivo)
    print(f"Gráfico de ângulos salvo em: {caminho_completo_arquivo}")
    return fig

def gerar_grafico_posicao_quadril(dados_csv, fps, initial_y_quadril=None, altura_frame_ref=None, limiar_queda_y_percentual=None, nome_arquivo="posicao_quadril_agachamento.html"): # Novo parâmetro
    """
    Gera e salva um gráfico interativo (Plotly) de série temporal da posição Y do quadril.
    """
    if dados_csv is None:
        print("Dados CSV não disponíveis para gerar o gráfico de posição do quadril.")
        return None

    df = pd.DataFrame(dados_csv)
    df['Quadril_Esquerdo_Y_Px'] = pd.to_numeric(df['Quadril_Esquerdo_Y_Px'], errors='coerce')
    df['Quadril_Direito_Y_Px'] = pd.to_numeric(df['Quadril_Direito_Y_Px'], errors='coerce')
    df['Frame'] = pd.to_numeric(df['Frame'], errors='coerce')
    df['Tempo_Segundos'] = df['Frame'] / fps
    df['Avg_Quadril_Y_Px'] = (df['Quadril_Esquerdo_Y_Px'] + df['Quadril_Direito_Y_Px']) / 2

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Tempo_Segundos'], y=df['Avg_Quadril_Y_Px'], mode='lines', name='Média Quadril Y', line=dict(color='purple')))
    
    if initial_y_quadril is not None:
        fig.add_hline(y=initial_y_quadril, line_dash="dash", line_color="orange", annotation_text=f'Quadril Y Calibrado ({initial_y_quadril:.2f}px)', annotation_position="bottom left")
        
        # Usar o novo parâmetro de limiar
        if altura_frame_ref is not None and limiar_queda_y_percentual is not None:
            limiar_agachado_y = initial_y_quadril + altura_frame_ref * limiar_queda_y_percentual
            fig.add_hline(y=limiar_agachado_y, line_dash="dot", line_color="red", annotation_text=f'Limiar Agachado Y ({limiar_agachado_y:.2f}px)', annotation_position="top left")

    fig.update_layout(
        title='Variação da Posição Y Média do Quadril ao Longo do Tempo',
        xaxis_title='Tempo (segundos)',
        yaxis_title='Posição Y (pixels)',
        yaxis=dict(autorange='reversed'),
        hovermode="x unified",
        height=500
    )
    
    diretorio_relatorios = _garantir_diretorio_relatorios_existe()
    caminho_completo_arquivo = os.path.join(diretorio_relatorios, nome_arquivo)
    fig.write_html(caminho_completo_arquivo)
    print(f"Gráfico de posição do quadril salvo em: {caminho_completo_arquivo}")
    return fig

def gerar_grafico_duracao_agachamentos(lista_agachamentos, transicoes_em_pe, nome_arquivo="duracao_agachamentos.html"): # Agora recebe transicoes_em_pe
    """
    Gera e salva um gráfico de pontos com linhas (Plotly) da duração de cada agachamento
    e do tempo em pé entre eles.
    """
    if not lista_agachamentos and not transicoes_em_pe:
        print("Nenhum agachamento ou transição detectado para gerar o gráfico de duração.")
        return None

    # Combinar dados de agachamento e tempo em pé
    dados_combinados = []
    
    # Adiciona uma transição "início" se houver agachamentos
    if lista_agachamentos and transicoes_em_pe and transicoes_em_pe[0]['inicio_frame'] < lista_agachamentos[0]['inicio_frame']:
        # Se a primeira transição em pé for antes do primeiro agachamento, inclua
        dados_combinados.append({
            'tipo': 'Em Pé (pré-agachamento)',
            'numero_seq': 0.5, # Ponto intermediário
            'duracao_segundos': transicoes_em_pe[0]['duracao_segundos'],
            'cor': 'blue'
        })
    
    agachamento_idx = 0
    transicao_idx = 0
    
    while agachamento_idx < len(lista_agachamentos) or transicao_idx < len(transicoes_em_pe):
        # Decide se adiciona um agachamento ou uma transição em pé
        if agachamento_idx < len(lista_agachamentos):
            squat = lista_agachamentos[agachamento_idx]
            dados_combinados.append({
                'tipo': f'Agach. {squat["numero"]}',
                'numero_seq': squat["numero"],
                'duracao_segundos': squat['duracao_segundos'],
                'cor': 'green' # Cor para agachamento
            })
            agachamento_idx += 1
        
        if transicao_idx < len(transicoes_em_pe):
            transicao = transicoes_em_pe[transicao_idx]
            # Associa a transição ao agachamento que a segue, ou a um ponto após o agachamento anterior
            if agachamento_idx > 0: # Se já adicionamos pelo menos um agachamento
                 dados_combinados.append({
                    'tipo': f'Em Pé (após Agach. {agachamento_idx})',
                    'numero_seq': agachamento_idx + 0.5, # Ponto entre agachamentos
                    'duracao_segundos': transicao['duracao_segundos'],
                    'cor': 'orange' # Cor para tempo em pé
                })
            else: # Se for a primeira transição em pé antes do primeiro agachamento
                 dados_combinados.append({
                    'tipo': f'Em Pé (início)',
                    'numero_seq': 0.5, # Ponto antes do primeiro agachamento
                    'duracao_segundos': transicao['duracao_segundos'],
                    'cor': 'orange' # Cor para tempo em pé
                })
            transicao_idx += 1

    df_combinado = pd.DataFrame(dados_combinados)
    
    # Ordena para garantir que a linha conecte na ordem correta
    df_combinado = df_combinado.sort_values(by='numero_seq')

    fig = go.Figure()

    # Adicionar traço de linha principal
    fig.add_trace(go.Scatter(
        x=df_combinado['tipo'], # Usar tipo para o eixo X com rótulos
        y=df_combinado['duracao_segundos'],
        mode='lines+markers', # Linhas e pontos
        marker=dict(size=10, color=df_combinado['cor']), # Cor dos pontos
        line=dict(color='grey', width=2), # Cor da linha
        name='Duração'
    ))

    fig.update_layout(
        title='Duração de Cada Agachamento e Tempo em Pé',
        xaxis_title='Evento (Agachamento / Em Pé)',
        yaxis_title='Duração (segundos)',
        hovermode="x unified",
        height=550 # Altura ajustada
    )
    
    diretorio_relatorios = _garantir_diretorio_relatorios_existe()
    caminho_completo_arquivo = os.path.join(diretorio_relatorios, nome_arquivo)
    fig.write_html(caminho_completo_arquivo)
    print(f"Gráfico de duração dos agachamentos salvo em: {caminho_completo_arquivo}")
    return fig # Retorna o objeto figura do plotly