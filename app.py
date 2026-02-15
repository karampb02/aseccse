"""
Flask Application for Spotify to YouTube Playlist Converter
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from config import Config
from spotify_service import SpotifyService
from youtube_service import YouTubeService
import os

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY

# Initialize services
spotify_service = SpotifyService()
youtube_service = YouTubeService()


@app.route('/')
def index():
    """Home page"""
    return render_template('index.html',
                         spotify_connected=session.get('spotify_token') is not None,
                         youtube_connected=session.get('youtube_credentials') is not None)


@app.route('/connect/spotify')
def connect_spotify():
    """Redirect to Spotify authentication"""
    auth_url = spotify_service.get_auth_url()
    return redirect(auth_url)


@app.route('/spotify/callback')
def spotify_callback():
    """Handle Spotify OAuth callback"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return f"Error: {error}", 400
    
    if code:
        try:
            token = spotify_service.get_access_token(code)
            session['spotify_token'] = token
            spotify_service.set_access_token(token)
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    return "No code provided", 400


@app.route('/connect/youtube')
def connect_youtube():
    """Redirect to YouTube authentication"""
    auth_url, state = youtube_service.get_auth_url()
    session['youtube_state'] = state
    return redirect(auth_url)


@app.route('/youtube/callback')
def youtube_callback():
    """Handle YouTube OAuth callback"""
    code = request.args.get('code')
    state = request.args.get('state')
    error = request.args.get('error')
    
    if error:
        return f"Error: {error}", 400
    
    if code:
        try:
            stored_state = session.get('youtube_state')
            if state != stored_state:
                return "State mismatch error", 400
            
            credentials = youtube_service.get_credentials(code, state)
            # Store credentials in session (in production, use a proper storage)
            session['youtube_credentials'] = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes
            }
            youtube_service.set_credentials(credentials)
            return redirect(url_for('index'))
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    return "No code provided", 400


@app.route('/playlists')
def get_playlists():
    """Get user's Spotify playlists"""
    if 'spotify_token' not in session:
        return jsonify({'error': 'Not connected to Spotify'}), 401
    
    try:
        spotify_service.set_access_token(session['spotify_token'])
        playlists = spotify_service.get_user_playlists()
        
        # Format playlists for display
        formatted_playlists = [
            {
                'id': pl['id'],
                'name': pl['name'],
                'tracks': pl['tracks']['total'],
                'image': pl['images'][0]['url'] if pl['images'] else None
            }
            for pl in playlists
        ]
        
        return jsonify(formatted_playlists)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert', methods=['POST'])
def convert_playlist():
    """Convert a Spotify playlist to YouTube"""
    if 'spotify_token' not in session:
        return jsonify({'error': 'Not connected to Spotify'}), 401
    
    if 'youtube_credentials' not in session:
        return jsonify({'error': 'Not connected to YouTube'}), 401
    
    data = request.json
    playlist_id = data.get('playlist_id')
    
    if not playlist_id:
        return jsonify({'error': 'No playlist_id provided'}), 400
    
    try:
        # Set up services
        spotify_service.set_access_token(session['spotify_token'])
        
        # Reconstruct YouTube credentials from session
        from google.oauth2.credentials import Credentials
        creds_data = session['youtube_credentials']
        credentials = Credentials(
            token=creds_data['token'],
            refresh_token=creds_data.get('refresh_token'),
            token_uri=creds_data['token_uri'],
            client_id=creds_data['client_id'],
            client_secret=creds_data['client_secret'],
            scopes=creds_data['scopes']
        )
        youtube_service.set_credentials(credentials)
        
        # Get playlist details and tracks
        playlist_details = spotify_service.get_playlist_details(playlist_id)
        tracks = spotify_service.get_playlist_tracks(playlist_id)
        
        # Create YouTube playlist
        youtube_playlist_name = f"{playlist_details['name']} (from Spotify)"
        description = f"Converted from Spotify playlist. Original had {len(tracks)} tracks."
        
        result = youtube_service.create_playlist_from_songs(
            youtube_playlist_name,
            tracks,
            description
        )
        
        return jsonify({
            'success': True,
            'playlist_id': result['playlist_id'],
            'playlist_url': f"https://www.youtube.com/playlist?list={result['playlist_id']}",
            'total_songs': result['total_songs'],
            'added_count': result['added_count'],
            'failed_songs': result['failed_songs']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/disconnect/spotify')
def disconnect_spotify():
    """Disconnect Spotify"""
    session.pop('spotify_token', None)
    return redirect(url_for('index'))


@app.route('/disconnect/youtube')
def disconnect_youtube():
    """Disconnect YouTube"""
    session.pop('youtube_credentials', None)
    session.pop('youtube_state', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
