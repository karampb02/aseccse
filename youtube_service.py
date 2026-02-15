"""
YouTube Service Module
Handles all YouTube API interactions including authentication, search, and playlist creation
"""
import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from config import Config


class YouTubeService:
    """Service class for YouTube API operations"""
    
    def __init__(self):
        """Initialize YouTube service"""
        self.credentials = None
        self.youtube = None
    
    def get_auth_flow(self, state=None):
        """Create and return OAuth flow for YouTube authentication"""
        # Create credentials dict from config
        client_config = {
            "web": {
                "client_id": Config.YOUTUBE_CLIENT_ID,
                "client_secret": Config.YOUTUBE_CLIENT_SECRET,
                "redirect_uris": [Config.YOUTUBE_REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
        
        flow = Flow.from_client_config(
            client_config,
            scopes=Config.YOUTUBE_SCOPES,
            redirect_uri=Config.YOUTUBE_REDIRECT_URI
        )
        
        if state:
            flow.state = state
        
        return flow
    
    def get_auth_url(self):
        """Get YouTube authorization URL"""
        flow = self.get_auth_flow()
        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return auth_url, state
    
    def get_credentials(self, code, state):
        """Exchange authorization code for credentials"""
        flow = self.get_auth_flow(state)
        flow.fetch_token(code=code)
        return flow.credentials
    
    def set_credentials(self, credentials):
        """Set credentials and build YouTube client"""
        self.credentials = credentials
        self.youtube = build(
            Config.YOUTUBE_API_SERVICE_NAME,
            Config.YOUTUBE_API_VERSION,
            credentials=credentials
        )
    
    def search_video(self, query, max_results=1):
        """
        Search for a video on YouTube
        
        Args:
            query: Search query string (e.g., "Artist - Song Name")
            max_results: Maximum number of results to return
            
        Returns:
            Video ID of the first result, or None if not found
        """
        if not self.youtube:
            raise Exception("Not authenticated with YouTube")
        
        try:
            request = self.youtube.search().list(
                part="snippet",
                maxResults=max_results,
                q=query,
                type="video"
            )
            response = request.execute()
            
            if response['items']:
                return response['items'][0]['id']['videoId']
            else:
                return None
        except Exception as e:
            print(f"Error searching for '{query}': {str(e)}")
            return None
    
    def create_playlist(self, title, description="", privacy_status="private"):
        """
        Create a new YouTube playlist
        
        Args:
            title: Playlist title
            description: Playlist description
            privacy_status: Privacy setting (private, public, or unlisted)
            
        Returns:
            Playlist ID of the newly created playlist
        """
        if not self.youtube:
            raise Exception("Not authenticated with YouTube")
        
        request = self.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description
                },
                "status": {
                    "privacyStatus": privacy_status
                }
            }
        )
        response = request.execute()
        return response['id']
    
    def add_video_to_playlist(self, playlist_id, video_id):
        """
        Add a video to a playlist
        
        Args:
            playlist_id: YouTube playlist ID
            video_id: YouTube video ID to add
            
        Returns:
            True if successful, False otherwise
        """
        if not self.youtube:
            raise Exception("Not authenticated with YouTube")
        
        try:
            request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": video_id
                        }
                    }
                }
            )
            request.execute()
            return True
        except Exception as e:
            print(f"Error adding video {video_id} to playlist: {str(e)}")
            return False
    
    def create_playlist_from_songs(self, playlist_name, songs, description=""):
        """
        Create a YouTube playlist and populate it with songs
        
        Args:
            playlist_name: Name for the new playlist
            songs: List of song strings to search for and add
            description: Playlist description
            
        Returns:
            Dict with playlist_id, added_count, failed_songs
        """
        if not self.youtube:
            raise Exception("Not authenticated with YouTube")
        
        # Create the playlist
        playlist_id = self.create_playlist(playlist_name, description)
        
        added_count = 0
        failed_songs = []
        
        # Add each song
        for song in songs:
            video_id = self.search_video(song)
            
            if video_id:
                success = self.add_video_to_playlist(playlist_id, video_id)
                if success:
                    added_count += 1
                    print(f"Added: {song}")
                else:
                    failed_songs.append(song)
                    print(f"Failed to add: {song}")
            else:
                failed_songs.append(song)
                print(f"Could not find: {song}")
        
        return {
            'playlist_id': playlist_id,
            'added_count': added_count,
            'failed_songs': failed_songs,
            'total_songs': len(songs)
        }
