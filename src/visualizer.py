import cv2
import pandas as pd
import os
from .config import RAW_DATA_DIR, PROCESSED_DATA_DIR, STATS_DIR

def create_video_overlay(video_filename):
    video_path = os.path.join(RAW_DATA_DIR, video_filename)
    csv_path = os.path.join(STATS_DIR, video_filename.replace('.mp4', '.csv'))
    output_path = os.path.join(PROCESSED_DATA_DIR, 'output_' + video_filename)

    if not os.path.exists(csv_path): return
    
    df = pd.read_csv(csv_path)
    coords = {row['frame']: (int(row['x']), int(row['y'])) for _, row in df.iterrows()}
    
    cap = cv2.VideoCapture(video_path)
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), cap.get(cv2.CAP_PROP_FPS), 
                          (int(cap.get(3)), int(cap.get(4))))
    
    print(f"🎬 Renderizando vídeo final...")
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret: break
        if idx in coords:
            cv2.circle(frame, coords[idx], 8, (0, 0, 255), -1)
        out.write(frame)
        idx += 1
    
    cap.release()
    out.release()
