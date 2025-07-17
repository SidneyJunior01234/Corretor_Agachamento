import os

FPS = 30

# --- CONFIGURAÇÃO DO DETECTOR DE POSE --
MDC = 0.5
MTC = 0.5

# --- THRESHOLDS ---
TOLERANCIA_PES_OMBRO_PERCENTUAL = 0.35
THRESHOLD_ANGULO_JOELHO_EM_PE = 150  
THRESHOLD_ANGULO_JOELHO_AGACHADO = 130 
Y_DROP_THRESHOLD_PX = 0.08

# --- Cores para o Desenho do Avatar (BGR) ---
COR_AMARELO = (0, 255, 255) # Default para "avatar"
COR_VERDE = (0, 255, 0)     # Para quando a pessoa está agachada
COR_VERMELHO = (0, 0, 255)  # Para erro de pés quando em pé

# --- ESTADOS DURANTE AGACHAMENTO ---
ESTADOS_DICT = {"Em Pe":0, "Transicao/Indefinido":1, "Agachado":2}

# --- Configurações de CSV ---
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.abspath(os.path.join(_CURRENT_DIR, '..', '..')) # Sobe 3 níveis da pasta 'app'

_DATA_DIR = os.path.join(_PROJECT_ROOT, 'dados')
CSV_FILE_NAME = os.path.join(_DATA_DIR, 'parametros', 'parametros.csv')

CSV_HEADERS = [
    'Frame',
    'Estado',
    'Angulo_Joelho_Esquerdo',
    'Angulo_Joelho_Direito',
    'Angulo_Tornozelo_Esquerdo',
    'Angulo_Tornozelo_Direito',
    'Distancia_Pes_Px',
    'Distancia_Ombros_Px',
    'Ombro_Esquerdo_Y_Px',
    'Ombro_Direito_Y_Px',
    'Quadril_Esquerdo_Y_Px',
    'Quadril_Direito_Y_Px'
]