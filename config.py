import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Flask
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Spotify
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
    SPOTIFY_REDIRECT_URI = os.environ.get('SPOTIFY_REDIRECT_URI', 'http://localhost:5000/spotify/callback')
    SPOTIFY_SCOPE = 'playlist-read-private playlist-read-collaborative'
    
    # YouTube
    YOUTUBE_CLIENT_ID = os.environ.get('YOUTUBE_CLIENT_ID')
    YOUTUBE_CLIENT_SECRET = os.environ.get('YOUTUBE_CLIENT_SECRET')
    YOUTUBE_REDIRECT_URI = os.environ.get('YOUTUBE_REDIRECT_URI', 'http://localhost:5000/youtube/callback')
    YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
    
    # API Configuration
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
