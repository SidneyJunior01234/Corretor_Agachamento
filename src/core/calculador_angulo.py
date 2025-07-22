# src/core/calculador_angulo.py

import math

def calcular_angulo(ponto_a, ponto_b, ponto_c):
    """
    Calcula o ângulo em graus entre três pontos (A, B, C), onde B é o vértice.
    
    Args:
        ponto_a (mediapipe.framework.formats.landmark_pb2.NormalizedLandmark): Primeiro ponto.
        ponto_b (mediapipe.framework.formats.landmark_pb2.NormalizedLandmark): Vértice (ponto central).
        ponto_c (mediapipe.framework.formats.landmark_pb2.NormalizedLandmark): Terceiro ponto.
        
    Returns:
        float: O ângulo em graus (entre 0 e 180).
    """
    ax, ay = ponto_a.x, ponto_a.y
    bx, by = ponto_b.x, ponto_b.y
    cx, cy = ponto_c.x, ponto_c.y

    angulo_radianos = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
    angulo_graus = math.degrees(angulo_radianos)

    if angulo_graus < 0:
        angulo_graus += 360
    
    # Ajusta o ângulo para ser o interno, garantindo valor entre 0 e 180
    if angulo_graus > 180:
        angulo_graus = 360 - angulo_graus

    return angulo_graus