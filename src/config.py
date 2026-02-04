import os

# Caminhos Absolutos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
WEIGHTS_PATH = os.path.join(BASE_DIR, 'models', 'weights', 'model_best.h5') # Exemplo Keras

# Configurações do Modelo
TARGET_WIDTH = 640   # TrackNet geralmente treina com essa resolução
TARGET_HEIGHT = 360
FPS_TARGET = 60      # Ideal para Tênis