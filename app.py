# app.py

import streamlit as st
import cv2
import numpy as np
import os
import time
import plotly.graph_objects as go # Importar para usar st.plotly_chart

# Importar funcionalidades dos módulos reorganizados
from src.core.detector_pose import DetectorPose
from src.core.analisador_agachamento import AnalisadorAgachamento
from src.visualizacao.desenhista_cv2 import desenhar_landmarks
from src.manipulador_dados.gerenciador_csv import inicializar_csv, adicionar_linha_csv, carregar_dados_csv
from src.visualizacao.gerador_graficos import (
    gerar_grafico_angulos,
    gerar_grafico_posicao_quadril,
    gerar_grafico_duracao_agachamentos
)
from config.configuracoes import (
    NOME_ARQUIVO_CSV,
    ESTADOS_DICT,
    COR_AMARELO, COR_VERDE, COR_VERMELHO,
    TOLERANCIA_PES_OMBRO_PERCENTUAL
)

st.set_page_config(layout="wide", page_title="Corretor de Agachamento")

st.title("🏋️ Corretor de Agachamento")

st.write("""
    Este aplicativo usa visão computacional para analisar a forma do seu agachamento
    e gerar um relatório completo ao final.
""")

# --- Controles da Barra Lateral ---
st.sidebar.header("Controles do Aplicativo")

# Opção de upload de vídeo ou usar exemplo
opcao_video = st.sidebar.radio(
    "Escolha a fonte do vídeo:",
    ("Upload de Vídeo", "Usar Vídeo de Exemplo")
)

caminho_video_exemplo = os.path.join('data', 'brutos', 'agachamento.mp4')
if not os.path.exists(os.path.dirname(caminho_video_exemplo)):
    os.makedirs(os.path.dirname(caminho_video_exemplo))

uploaded_file = None
if opcao_video == "Upload de Vídeo":
    uploaded_file = st.sidebar.file_uploader("Carregue seu vídeo de agachamento (mp4)", type=["mp4"])
    if uploaded_file:
        caminho_temp_upload_dir = "temp_upload"
        if not os.path.exists(caminho_temp_upload_dir):
            os.makedirs(caminho_temp_upload_dir)
        
        caminho_video = os.path.join(caminho_temp_upload_dir, uploaded_file.name)
        with open(caminho_video, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"Vídeo '{uploaded_file.name}' carregado com sucesso!")
    else:
        st.stop()
elif opcao_video == "Usar Vídeo de Exemplo":
    if os.path.exists(caminho_video_exemplo):
        caminho_video = caminho_video_exemplo
        st.sidebar.info(f"Usando vídeo de exemplo: `{caminho_video_exemplo}`")
    else:
        st.error(f"Vídeo de exemplo não encontrado em `{caminho_video_exemplo}`. Por favor, carregue um vídeo ou forneça o arquivo.")
        st.stop()
else:
    st.stop()

st.sidebar.markdown("---")
st.sidebar.subheader("Ajustes de Limiares para Agachamento")

# Sliders para os limiares
# Valores padrão: Em Pe (150-180), Agachado (0-130), Queda Y (0.05-0.15)
limiar_joelho_em_pe = st.sidebar.slider(
    'Ângulo Mín. Joelho "Em Pé" (graus)',
    min_value=120, max_value=180, value=150, step=1,
    help='Ângulo mínimo que o joelho deve atingir para ser considerado "Em Pé". Valores maiores exigem extensão maior.'
)

limiar_joelho_agachado = st.sidebar.slider(
    'Ângulo Máx. Joelho "Agachado" (graus)',
    min_value=40, max_value=195, value=120, step=1,
    help='Ângulo máximo que o joelho deve atingir para ser considerado "Agachado". Valores menores exigem agachamento mais profundo.'
)

limiar_queda_y_percentual = st.sidebar.slider(
    'Queda do Quadril para Agachamento (%)',
    min_value=0.03, max_value=0.20, value=0.05, step=0.01, format="%.2f",
    help='Percentual da altura do corpo que o quadril deve descer para o agachamento ser válido. Valores maiores exigem mais profundidade.'
)

st.sidebar.markdown("---")
processar_button = st.sidebar.button("Iniciar Análise do Agachamento")

placeholder_video = st.empty()
progress_bar_placeholder = st.empty()


if processar_button and caminho_video:
    detector = DetectorPose()
    analisador = AnalisadorAgachamento()
    
    caminho_csv_completo = inicializar_csv()
    
    cap = cv2.VideoCapture(caminho_video)
    
    if not cap.isOpened():
        st.error(f"Não foi possível abrir o vídeo: {caminho_video}")
        if 'temp_upload' in caminho_video:
            os.remove(caminho_video)
            os.rmdir(os.path.dirname(caminho_video))
        st.stop()

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if fps == 0:
        fps = 30.0
    
    frame_count = 0
    altura_frame_calibrada = None

    st.markdown("### Processando Vídeo e Analisando Agachamento...")
    st_progress_text = progress_bar_placeholder.text("Iniciando...")
    st_progress_bar = progress_bar_placeholder.progress(0)

    analisador.resetar_estado()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        st_progress_bar.progress(min(frame_count / total_frames, 1.0))
        st_progress_text.text(f"Processando Frame: {frame_count}/{total_frames}")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = detector.processar_frame(frame_rgb)

        h, w, _ = frame.shape
        if altura_frame_calibrada is None:
            altura_frame_calibrada = h

        drawing_color = COR_AMARELO

        info_agachamento = None
        if resultados.pose_landmarks:
            # Passar os limiares do slider para o analisador
            info_agachamento = analisador.analisar_pose(
                resultados.pose_landmarks.landmark, h, w,
                limiar_joelho_em_pe, limiar_joelho_agachado, limiar_queda_y_percentual
            )
            
            estado_atual = info_agachamento['estado_pose']
            
            if estado_atual == "Agachado":
                drawing_color = COR_VERDE
            elif estado_atual == "Em Pe":
                dist_ombros_px = info_agachamento['distancia_ombros_px']
                dist_pes_px = info_agachamento['distancia_pes_px']
                limite_inferior_pes = dist_ombros_px * (1 - TOLERANCIA_PES_OMBRO_PERCENTUAL)
                limite_superior_pes = dist_ombros_px * (1 + TOLERANCIA_PES_OMBRO_PERCENTUAL)

                if not (limite_inferior_pes <= dist_pes_px <= limite_superior_pes):
                    drawing_color = COR_VERMELHO
                else:
                    drawing_color = COR_AMARELO

            else:
                drawing_color = COR_AMARELO

            frame = desenhar_landmarks(frame, resultados, drawing_color)
            
            linha_csv = [
                frame_count,
                ESTADOS_DICT[info_agachamento['estado_pose']],
                f"{info_agachamento['angulo_joelho_esq']:.2f}",
                f"{info_agachamento['angulo_joelho_dir']:.2f}",
                f"{info_agachamento['angulo_tornozelo_esq']:.2f}",
                f"{info_agachamento['angulo_tornozelo_dir']:.2f}",
                f"{info_agachamento['distancia_pes_px']:.2f}",
                f"{info_agachamento['distancia_ombros_px']:.2f}",
                f"{info_agachamento['ombro_esq_y_px']}",
                f"{info_agachamento['ombro_dir_y_px']}",
                f"{info_agachamento['quadril_esq_y_px']}",
                f"{info_agachamento['quadril_dir_y_px']}"
            ]
            adicionar_linha_csv(linha_csv, caminho_csv_completo)

        frame = cv2.resize(frame, (640, 480)) # Ajuste aqui para o tamanho desejado
        placeholder_video.image(frame, channels="BGR", use_container_width=True)
        # time.sleep(1/fps) # Pode causar lentidão, especialmente com vídeos grandes. Comente se necessário.

    cap.release()
    detector.fechar()
    
    if uploaded_file and os.path.exists(caminho_video):
        os.remove(caminho_video)
        if os.path.exists(caminho_temp_upload_dir) and not os.listdir(caminho_temp_upload_dir):
            os.rmdir(caminho_temp_upload_dir)

    st_progress_text.empty()
    st_progress_bar.empty()
    
    st.success("Análise do agachamento concluída! Gerando relatório...")

    # --- Análise Final e Geração de Relatórios ---
    st.markdown("---")
    st.markdown("## ✅ Relatório Final do Agachamento")
    
    dados_carregados = carregar_dados_csv(caminho_csv_completo)

    if dados_carregados:
        tempo_total_em_pe_seg = analisador.calcular_tempo_total_em_pe(dados_carregados, fps)
        st.write(f"**Tempo total em pé geral:** {tempo_total_em_pe_seg:.2f} segundos")
        
        lista_agachamentos, transicoes_em_pe = analisador.analisar_agachamentos_individuais(dados_carregados, fps)
        
        if lista_agachamentos or transicoes_em_pe:
            st.markdown("### Gráficos de Desempenho:")
            
            # Gráfico de Ângulos (Plotly) - Passar os limiares do slider
            fig_angulos = gerar_grafico_angulos(dados_carregados, fps, limiar_joelho_em_pe, limiar_joelho_agachado, nome_arquivo="angulos_agachamento.html")
            if fig_angulos:
                st.plotly_chart(fig_angulos, use_container_width=True)
            else:
                st.warning("Não foi possível gerar o gráfico de ângulos.")

            # Gráfico de Posição do Quadril (Plotly) - Passar o limiar do slider
            fig_quadril = gerar_grafico_posicao_quadril(dados_carregados, fps, analisador.initial_y_quadril, altura_frame_calibrada, limiar_queda_y_percentual, nome_arquivo="posicao_quadril_agachamento.html")
            if fig_quadril:
                st.plotly_chart(fig_quadril, use_container_width=True)
            else:
                st.warning("Não foi possível gerar o gráfico de posição do quadril.")
            
            # Gráfico de Duração de Agachamentos e Tempo em Pé (Plotly)
            fig_duracao = gerar_grafico_duracao_agachamentos(lista_agachamentos, transicoes_em_pe, nome_arquivo="duracao_agachamentos_interativo.html")
            if fig_duracao:
                st.plotly_chart(fig_duracao, use_container_width=True)
            else:
                st.warning("Não foi possível gerar o gráfico de duração dos agachamentos e tempo em pé.")

            st.success("Relatórios e gráficos gerados com sucesso na pasta `data/relatorios`!")
        else:
            st.warning("Nenhum agachamento completo ou período em pé detectado para gerar relatório detalhado.")
    else:
        st.error("Não foi possível carregar os dados do CSV para o relatório final.")