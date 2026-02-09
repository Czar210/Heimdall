import os
import yt_dlp
from .config import RAW_DATA_DIR

class YouTubeIngester:
    def __init__(self, channel_url):
        self.channel_url = channel_url
        self.output_dir = RAW_DATA_DIR

    def download_latest_videos(self, limit=1):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.output_dir, '%(upload_date)s_%(title)s.%(ext)s'),
            'playlistend': limit,
            'ignoreerrors': True,
        }
        print(f"📥 Baixando {limit} vídeo(s) de {self.channel_url}...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.channel_url])