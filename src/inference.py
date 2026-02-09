import os
import cv2
import torch
import numpy as np
import pandas as pd
from collections import deque
from tqdm import tqdm
from .config import WEIGHTS_PATH, STATS_DIR, RAW_DATA_DIR
from .tracknet import TrackNet

class TrackNetInference:
    def __init__(self, weights_path=WEIGHTS_PATH):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f"🚀 Iniciando TrackNet em: {self.device}")
        
        self.model = TrackNet().to(self.device)
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"❌ Pesos não encontrados em: {weights_path}. Baixe o modelo!")
            
        checkpoint = torch.load(weights_path, map_location=self.device)
        state_dict = checkpoint['state_dict'] if 'state_dict' in checkpoint else checkpoint
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def preprocess(self, frames):
        # Converte 3 frames para Tensor (1, 9, 360, 640)
        imgs = []
        for f in frames:
            img = cv2.resize(f, (640, 360))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgs.append(img.transpose(2, 0, 1))
        input_tensor = np.concatenate(imgs, axis=0)
        input_tensor = input_tensor.astype(np.float32) / 255.0
        return torch.from_numpy(input_tensor).unsqueeze(0).to(self.device)

    def predict_video(self, video_filename):
        video_path = os.path.join(RAW_DATA_DIR, video_filename)
        output_csv = os.path.join(STATS_DIR, video_filename.replace('.mp4', '.csv'))
        
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        orig_w, orig_h = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        print(f"🎾 Analisando: {video_filename}...")
        frame_buffer, detections = deque(maxlen=3), []
        pbar = tqdm(total=total_frames)
        
        with torch.no_grad():
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret: break
                frame_buffer.append(frame)
                
                if len(frame_buffer) == 3:
                    out = self.model(self.preprocess(list(frame_buffer)))
                    heatmap = out.squeeze().cpu().numpy()
                    
                    # Pós-processamento (Heatmap -> Coordenada)
                    idx = np.argmax(heatmap)
                    y, x = np.unravel_index(idx, heatmap.shape)
                    if heatmap[y, x] > 0.5: # Confiança mínima
                        detections.append({
                            'frame': frame_idx - 1,
                            'x': int(x * (orig_w / 640)),
                            'y': int(y * (orig_h / 360))
                        })
                frame_idx += 1
                pbar.update(1)
        
        cap.release()
        pd.DataFrame(detections).to_csv(output_csv, index=False)
        print(f"✅ CSV Salvo: {output_csv}")
