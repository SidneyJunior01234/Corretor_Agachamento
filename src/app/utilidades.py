import csv
import math

from .parametros import*

# --- Função para calcular o ângulo entre três pontos (A, B, C onde B é o vértice) ---
def calculate_angle(a, b, c):
    ax, ay = a.x, a.y
    bx, by = b.x, b.y
    cx, cy = c.x, c.y

    angle_radians = math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx)
    angle_degrees = math.degrees(angle_radians)

    if angle_degrees < 0:
        angle_degrees += 360
    
    # Ajusta o ângulo para ser o interno, garantindo valor entre 0 e 180
    if angle_degrees > 180:
        angle_degrees = 360 - angle_degrees

    return angle_degrees

# --- Funções de análise de CSV (mantidas para referência, idealmente em um arquivo separado) ---
def carregar_dados_csv(caminho_csv):
    data = []
    try:
        with open(caminho_csv, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f'Erro: O arquivo {caminho_csv} não foi encontrado.')
        return None
    
    if not data:
        print('Não há dados para analisar.')
        return None
    return data

def calcular_tempo_total_em_pe(dados_csv, fps):
    if dados_csv is None or fps <= 0:
        return 0

    total_frames_em_pe = 0
    for row in dados_csv:
        if int(row['Estado']) == ESTADOS_DICT['Em Pe']:
            total_frames_em_pe += 1
    
    tempo_total_em_pe_segundos = total_frames_em_pe / fps
    return tempo_total_em_pe_segundos

def analisar_agachamentos_individuais(dados_csv, fps):
    if dados_csv is None or fps <= 0:
        return []

    agachamentos = []
    agachamento_atual_start_frame = -1
    is_squatting = False

    for i, row in enumerate(dados_csv):
        frame_num = int(row['Frame'])
        estado = int(row['Estado'])

        if estado == ESTADOS_DICT['Agachado'] and not is_squatting:
            agachamento_atual_start_frame = frame_num
            is_squatting = True
        elif estado == ESTADOS_DICT['Em Pe'] and is_squatting:
            agachamento_end_frame = frame_num
            duration_frames = agachamento_end_frame - agachamento_atual_start_frame
            duration_seconds = duration_frames / fps
            agachamentos.append({
                'inicio_frame': agachamento_atual_start_frame,
                'fim_frame': agachamento_end_frame,
                'duracao_segundos': duration_seconds
            })
            is_squatting = False
    
    if is_squatting:
        duration_frames = int(dados_csv[-1]['Frame']) - agachamento_atual_start_frame
        duration_seconds = duration_frames / fps
        agachamentos.append({
            'inicio_frame': agachamento_atual_start_frame,
            'fim_frame': int(dados_csv[-1]['Frame']),
            'duracao_segundos': duration_seconds
        })
    
    return agachamentos
