import os
from src.ingestion import YouTubeIngester
from src.inference import TrackNetInference
from src.visualizer import create_video_overlay
from src.config import RAW_DATA_DIR

def main():
    # 1. Download
    downloader = YouTubeIngester("https://www.youtube.com/@gihan84")
    # Comente a linha abaixo se não quiser baixar novos vídeos toda vez
    downloader.download_latest_videos(limit=1) 

    # 2. Setup Modelo
    tracker = TrackNetInference()
    
    # 3. Processamento em Lote
    videos = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.mp4')]
    for video in videos:
        tracker.predict_video(video)     # Gera CSV
        create_video_overlay(video)      # Gera MP4 com bolinha

if __name__ == "__main__":
    main()