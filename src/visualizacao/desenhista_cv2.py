# src/visualizacao/desenhista_cv2.py

import cv2
import mediapipe as mp
from config.configuracoes import COR_AMARELO, COR_VERDE, COR_VERMELHO, ESTADOS_DICT

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def desenhar_landmarks(frame, resultados_pose, cor_desenho): # <--- Confirme se o nome é 'desenhar_landmarks' e os parâmetros
    """
    Desenha os landmarks da pose no frame com cores dinâmicas baseadas no estado do agachamento.
    
    Args:
        frame (numpy.ndarray): O frame do vídeo.
        resultados_pose (mediapipe.python.solution_base.SolutionOutputs): Resultados da detecção de pose.
        cor_desenho (tuple): A cor (BGR) para desenhar os landmarks.
    
    Returns:
        numpy.ndarray: O frame com os landmarks desenhados.
    """
    if resultados_pose.pose_landmarks:
        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=resultados_pose.pose_landmarks,
            connections=mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=cor_desenho, thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=cor_desenho, thickness=2, circle_radius=2)
        )
    return frame