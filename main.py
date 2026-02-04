import os
import cv2
from src.config import RAW_DATA_DIR
from src.ingestion import YouTubeIngester

def main():
    # 1. Pipeline de Ingestão
    # Comente esta linha se já tiver os vídeos para não baixar sempre
    downloader = YouTubeIngester(channel_url="https://www.youtube.com/@gihan84")
    # downloader.download_latest_videos(limit=1) 

    # 2. Pipeline de Processamento (Listar arquivos baixados)
    video_files = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.mp4')]
    
    if not video_files:
        print("⚠️ Nenhum vídeo encontrado em data/raw.")
        return

    print(f"🔍 Encontrados {len(video_files)} vídeos para processar.")

    # 3. Loop de Inferência (Placeholder para o TrackNet)
    for video_file in video_files:
        video_path = os.path.join(RAW_DATA_DIR, video_file)
        print(f"🎾 Processando: {video_file} ...")
        
        # Aqui chamaremos a classe de inferência (que vamos criar a seguir)
        # analyzer = TennisAnalyzer(video_path)
        # analyzer.run()

if __name__ == "__main__":
    main()