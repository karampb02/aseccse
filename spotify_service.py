"""
Spotify Service Module
Handles all Spotify API interactions including authentication and playlist fetching
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import Config


class SpotifyService:
    """Service class for Spotify API operations"""
    
    def __init__(self):
        """Initialize Spotify service with OAuth"""
        self.sp_oauth = SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope=Config.SPOTIFY_SCOPE
        )
        self.sp = None
    
    def get_auth_url(self):
        """Get Spotify authorization URL"""
        return self.sp_oauth.get_authorize_url()
    
    def get_access_token(self, code):
        """Exchange authorization code for access token"""
        token_info = self.sp_oauth.get_access_token(code)
        return token_info['access_token']
    
    def set_access_token(self, token):
        """Set access token for Spotify client"""
        self.sp = spotipy.Spotify(auth=token)
    
    def get_user_playlists(self):
        """Fetch all playlists for the authenticated user"""
        if not self.sp:
            raise Exception("Not authenticated with Spotify")
        
        playlists = []
        results = self.sp.current_user_playlists()
        
        while results:
            playlists.extend(results['items'])
            if results['next']:
                results = self.sp.next(results)
            else:
                results = None
        
        return playlists
    
    def get_playlist_tracks(self, playlist_id):
        """
        Fetch all tracks from a specific playlist
        
        Args:
            playlist_id: The Spotify playlist ID
            
        Returns:
            List of song strings in format "Artist - Track Name"
        """
        if not self.sp:
            raise Exception("Not authenticated with Spotify")
        
        tracks = []
        results = self.sp.playlist_tracks(playlist_id)
        
        while results:
            for item in results['items']:
                track = item['track']
                if track:  # Sometimes track can be None
                    # Get primary artist and track name
                    artist = track['artists'][0]['name'] if track['artists'] else 'Unknown Artist'
                    track_name = track['name']
                    tracks.append(f"{artist} - {track_name}")
            
            if results['next']:
                results = self.sp.next(results)
            else:
                results = None
        
        return tracks
    
    def get_playlist_details(self, playlist_id):
        """Get playlist details including name and description"""
        if not self.sp:
            raise Exception("Not authenticated with Spotify")
        
        playlist = self.sp.playlist(playlist_id)
        return {
            'name': playlist['name'],
            'description': playlist.get('description', ''),
            'total_tracks': playlist['tracks']['total']
        }
