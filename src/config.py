import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Diretórios de Dados
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
STATS_DIR = os.path.join(BASE_DIR, 'data', 'stats')

# Caminho do Modelo (O arquivo .pth deve ser baixado manualmente)
WEIGHTS_PATH = os.path.join(BASE_DIR, 'models', 'weights', 'TrackNet_best.pth')

# Garante que as pastas existam
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(STATS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(WEIGHTS_PATH), exist_ok=True)