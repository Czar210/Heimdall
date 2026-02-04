import os
import yt_dlp
from .config import RAW_DATA_DIR

class YouTubeIngester:
    def __init__(self, channel_url="https://www.youtube.com/@gihan84"):
        self.channel_url = channel_url
        self.output_dir = RAW_DATA_DIR

    def download_latest_videos(self, limit=5):
        """
        Baixa os últimos N vídeos do canal.
        """
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.output_dir, '%(upload_date)s_%(title)s.%(ext)s'),
            'playlistend': limit, # Baixa apenas os últimos 'limit' vídeos
            'ignoreerrors': True,
        }

        print(f"📥 Iniciando download de {limit} vídeos do canal {self.channel_url}...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.channel_url])
            
        print("✅ Downloads concluídos.")

if __name__ == "__main__":
    # Teste isolado
    ingester = YouTubeIngester()
    ingester.download_latest_videos(limit=2)