# src/core/analisador_agachamento.py

from src.core.calculador_angulo import calcular_angulo
from config.configuracoes import (
    TOLERANCIA_PES_OMBRO_PERCENTUAL,
    # REMOVIDOS OS LIMIARES FIXOS DAQUI, ELES SERÃO PASSADOS COMO PARÂMETRO
    ESTADOS_DICT
)
import mediapipe as mp

class AnalisadorAgachamento:
    """
    Analisa a pose para determinar o estado do agachamento e feedback.
    """
    def __init__(self):
        self.initial_y_quadril = None
        self.estado_anterior = "Transicao/Indefinido"

    def resetar_estado(self):
        """Reinicia o estado para uma nova sessão ou calibração."""
        self.initial_y_quadril = None
        self.estado_anterior = "Transicao/Indefinido"

    def analisar_pose(self, landmarks, altura_frame, largura_frame, 
                      limiar_joelho_em_pe, limiar_joelho_agachado, limiar_queda_y_percentual):
        """
        Analisa os landmarks da pose para determinar o estado do agachamento,
        usando limiares fornecidos.

        Args:
            landmarks (list): Lista de mediapipe.framework.formats.landmark_pb2.NormalizedLandmark.
            altura_frame (int): Altura do frame em pixels.
            largura_frame (int): Largura do frame em pixels.
            limiar_joelho_em_pe (float): Ângulo mínimo para ser considerado "Em Pé".
            limiar_joelho_agachado (float): Ângulo máximo para ser considerado "Agachado".
            limiar_queda_y_percentual (float): Percentual da queda do quadril para agachamento profundo.

        Returns:
            tuple: Dicionário com dados da análise.
        """
        
        om_esq = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
        om_dir = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        quadril_esq = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP]
        quadril_dir = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP]
        joelho_esq = landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE]
        joelho_dir = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE]
        tornozelo_esq = landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE]
        tornozelo_dir = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE]
        pe_esq = landmarks[mp.solutions.pose.PoseLandmark.LEFT_HEEL]
        pe_dir = landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HEEL]

        # --- Cálculos de Posições e Ângulos ---
        om_esq_y_px = int(om_esq.y * altura_frame)
        om_dir_y_px = int(om_dir.y * altura_frame)
        quadril_esq_y_px = int(quadril_esq.y * altura_frame)
        quadril_dir_y_px = int(quadril_dir.y * altura_frame)
        
        avg_quadril_y_px = (quadril_esq_y_px + quadril_dir_y_px) / 2

        if self.initial_y_quadril is None:
            self.initial_y_quadril = avg_quadril_y_px
            # Removido print para console, Streamlit gerencia
            # print(f"\n--- CALIBRAÇÃO INICIAL ---")
            # print(f"Posição Y inicial do quadril calibrada: {self.initial_y_quadril:.2f} pixels.")
            # print("Por favor, garanta que a pessoa está em pé no início do vídeo.")
            # print("---------------------------\n")

        angulo_joelho_esq = calcular_angulo(quadril_esq, joelho_esq, tornozelo_esq)
        angulo_joelho_dir = calcular_angulo(quadril_dir, joelho_dir, tornozelo_dir)
        avg_angulo_joelho = (angulo_joelho_esq + angulo_joelho_dir) / 2

        angulo_tornozelo_esq = calcular_angulo(joelho_esq, tornozelo_esq, pe_esq)
        angulo_tornozelo_dir = calcular_angulo(joelho_dir, tornozelo_dir, pe_dir)

        dist_ombros_px = abs(int(om_dir.x * largura_frame) - int(om_esq.x * largura_frame))
        dist_pes_px = abs(int(tornozelo_dir.x * largura_frame) - int(tornozelo_esq.x * largura_frame))
        
        # --- Detecção do Estado (Em Pé / Agachado) ---
        current_pose_state = "Transicao/Indefinido"
        
        # Limiar de queda do quadril para agachamento
        limiar_queda_y = self.initial_y_quadril + altura_frame * limiar_queda_y_percentual

        if (avg_angulo_joelho < limiar_joelho_agachado and
            self.initial_y_quadril is not None and
            avg_quadril_y_px > limiar_queda_y):
            current_pose_state = "Agachado"
        
        elif (avg_angulo_joelho > limiar_joelho_em_pe and
              self.initial_y_quadril is not None and 
              avg_quadril_y_px < (self.initial_y_quadril + altura_frame * (limiar_queda_y_percentual / 2))):
            current_pose_state = "Em Pe"
            
        # --- Verificação de Pés (feedback apenas no console) ---
        limite_inferior_pes = dist_ombros_px * (1 - TOLERANCIA_PES_OMBRO_PERCENTUAL)
        limite_superior_pes = dist_ombros_px * (1 + TOLERANCIA_PES_OMBRO_PERCENTUAL)

        feedback_pes = ""
        if not (limite_inferior_pes <= dist_pes_px <= limite_superior_pes):
            if dist_pes_px < limite_inferior_pes:
                feedback_pes = "Pés muito juntos. Abra mais!"
            else: 
                feedback_pes = "Pés muito afastados. Aproxime!"
        else:
            feedback_pes = "Pés na largura dos ombros (OK!)"

        # --- Feedback no Console ---
        feedback_console = {
            "estado": current_pose_state,
            "angulo_joelho_medio": f"{avg_angulo_joelho:.2f}",
            "posicao_quadril_y": f"{avg_quadril_y_px:.2f}",
            "distancia_ombros": f"{dist_ombros_px:.2f}",
            "distancia_pes": f"{dist_pes_px:.2f}",
            "feedback_pes": feedback_pes,
            "angulo_joelho_esq": f"{angulo_joelho_esq:.2f}",
            "angulo_joelho_dir": f"{angulo_joelho_dir:.2f}",
            "angulo_tornozelo_esq": f"{angulo_tornozelo_esq:.2f}",
            "angulo_tornozelo_dir": f"{angulo_tornozelo_dir:.2f}"
        }

        # Retorna todos os dados para serem salvos no CSV e usados para desenho
        return {
            'estado_pose': current_pose_state,
            'angulo_joelho_esq': angulo_joelho_esq,
            'angulo_joelho_dir': angulo_joelho_dir,
            'angulo_tornozelo_esq': angulo_tornozelo_esq,
            'angulo_tornozelo_dir': angulo_tornozelo_dir,
            'distancia_pes_px': dist_pes_px,
            'distancia_ombros_px': dist_ombros_px,
            'ombro_esq_y_px': om_esq_y_px,
            'ombro_dir_y_px': om_dir_y_px,
            'quadril_esq_y_px': quadril_esq_y_px,
            'quadril_dir_y_px': quadril_dir_y_px,
            'initial_y_quadril': self.initial_y_quadril, # Passa o valor calibrado
            'feedback_console': feedback_console
        }

    def calcular_tempo_total_em_pe(self, dados_csv, fps): 
        """
        Calcula o tempo total que a pessoa passou em pé.
        """
        if dados_csv is None or fps <= 0:
            return 0

        total_frames_em_pe = 0
        for row in dados_csv:
            try:
                estado_do_frame = int(row['Estado'])
            except ValueError:
                continue

            if estado_do_frame == ESTADOS_DICT['Em Pe']:
                total_frames_em_pe += 1

        tempo_total_em_pe_segundos = total_frames_em_pe / fps
        return tempo_total_em_pe_segundos

    def analisar_agachamentos_individuais(self, dados_csv, fps):
        """
        Analisa e retorna a duração de cada agachamento individual,
        além dos tempos em pé entre eles.
        """
        if dados_csv is None or fps <= 0:
            return [], []

        agachamentos_detectados = []
        transicoes_em_pe = []
        
        agachamento_atual_inicio_frame = -1
        esta_agachando = False
        
        # Variáveis para calcular tempo em pé entre agachamentos
        # Este será o frame onde a pessoa terminou de agachar e começou a ficar em pé
        ultimo_fim_agachamento_frame = -1 

        for i, linha in enumerate(dados_csv):
            num_frame = int(linha['Frame'])
            try:
                estado = int(linha['Estado'])
            except ValueError:
                continue

            if estado == ESTADOS_DICT['Agachado'] and not esta_agachando:
                # Início de um agachamento
                agachamento_atual_inicio_frame = num_frame
                esta_agachando = True
                
                # Se há um fim de agachamento anterior registrado,
                # calculamos o tempo em pé entre ele e o início do agachamento atual.
                if ultimo_fim_agachamento_frame != -1:
                    duracao_em_pe_frames = agachamento_atual_inicio_frame - ultimo_fim_agachamento_frame
                    if duracao_em_pe_frames > 0: # Garante duração positiva
                        transicoes_em_pe.append({
                            'inicio_frame': ultimo_fim_agachamento_frame,
                            'fim_frame': agachamento_atual_inicio_frame,
                            'duracao_segundos': duracao_em_pe_frames / fps
                        })
                    ultimo_fim_agachamento_frame = -1 # Reseta para o próximo ciclo

            elif estado == ESTADOS_DICT['Em Pe'] and esta_agachando:
                # Fim de um agachamento
                agachamento_fim_frame = num_frame
                duracao_frames = agachamento_fim_frame - agachamento_atual_inicio_frame
                agachamentos_detectados.append({
                    'tipo': 'agachamento',
                    'numero': len(agachamentos_detectados) + 1,
                    'inicio_frame': agachamento_atual_inicio_frame,
                    'fim_frame': agachamento_fim_frame,
                    'duracao_segundos': duracao_frames / fps
                })
                esta_agachando = False
                ultimo_fim_agachamento_frame = num_frame # Registra o frame onde terminou o agachamento e começou a ficar em pé
        
        # Lidar com agachamento que está ocorrendo no final do vídeo (se a pessoa ainda está agachando)
        if esta_agachando:
            try:
                ultimo_frame_video = int(dados_csv[-1]['Frame'])
            except (IndexError, ValueError):
                ultimo_frame_video = agachamento_atual_inicio_frame # Fallback
            
            duracao_frames = ultimo_frame_video - agachamento_atual_inicio_frame
            agachamentos_detectados.append({
                'tipo': 'agachamento',
                'numero': len(agachamentos_detectados) + 1,
                'inicio_frame': agachamento_atual_inicio_frame,
                'fim_frame': ultimo_frame_video,
                'duracao_segundos': duracao_frames / fps
            })
            # Não calculamos tempo em pé depois do último agachamento se o vídeo terminar agachando

        # Se houver um período em pé no início do vídeo ANTES do primeiro agachamento,
        # ou se o vídeo terminar em pé, isso não será mais considerado uma "transição entre agachamentos"
        # pela lógica acima. Isso torna o gráfico mais focado nas repetições e seus intervalos.
        
        return agachamentos_detectados, transicoes_em_pe