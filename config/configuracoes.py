# config/configuracoes.py

# --- THRESHOLDS E CONSTANTES ---
TOLERANCIA_PES_OMBRO_PERCENTUAL = 0.35
# LIMIAR_ANGULO_JOELHO_EM_PE = 150
# LIMIAR_ANGULO_JOELHO_AGACHADO = 130
# LIMIAR_QUEDA_Y_PX_PERCENTUAL = 0.08 # % da altura do frame

# --- CONFIGURAÇÕES DE CSV ---
NOME_ARQUIVO_CSV = 'dados_agachamento.csv'
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
# --- DICIONÁRIOS DE ESTADO ---
ESTADOS_DICT = {"Em Pe": 0, "Transicao/Indefinido": 1, "Agachado": 2}
# Dicionário inverso para facilitar a leitura dos estados em strings
ESTADOS_DICT_INV = {v: k for k, v in ESTADOS_DICT.items()}

# --- CORES PARA O AVATAR (BGR) ---
COR_AMARELO = (0, 255, 255)  # Default para "avatar"
COR_VERDE = (0, 255, 0)      # Para quando a pessoa está agachada
COR_VERMELHO = (0, 0, 255)   # Para erro de pés quando em pé

# --- CONFIGURAÇÕES DO MEDIA PIPE ---
MIN_CONFIDENCE_DETECCAO = 0.5
MIN_CONFIDENCE_RASTREAMENTO = 0.5