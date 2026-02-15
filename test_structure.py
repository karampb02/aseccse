#!/usr/bin/env python
"""
Simple test script to verify the application structure and imports
"""
import sys
import os

print("Testing Spotify to YouTube Converter...")
print("-" * 50)

# Test 1: Check if all required files exist
print("\n1. Checking required files...")
required_files = [
    'app.py',
    'config.py',
    'spotify_service.py',
    'youtube_service.py',
    'requirements.txt',
    '.env.example',
    '.gitignore',
    'README.md',
    'templates/index.html'
]

all_files_exist = True
for file in required_files:
    exists = os.path.exists(file)
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")
    if not exists:
        all_files_exist = False

if all_files_exist:
    print("  All required files present!")
else:
    print("  WARNING: Some files are missing!")
    sys.exit(1)

# Test 2: Check if modules can be imported
print("\n2. Testing module imports...")

# Set dummy environment variables for testing
os.environ.setdefault('SPOTIFY_CLIENT_ID', 'test_client_id')
os.environ.setdefault('SPOTIFY_CLIENT_SECRET', 'test_client_secret')
os.environ.setdefault('YOUTUBE_CLIENT_ID', 'test_client_id')
os.environ.setdefault('YOUTUBE_CLIENT_SECRET', 'test_client_secret')

try:
    import config
    print("  ✓ config.py")
except Exception as e:
    print(f"  ✗ config.py - {e}")
    sys.exit(1)

try:
    import spotify_service
    print("  ✓ spotify_service.py")
except Exception as e:
    print(f"  ✗ spotify_service.py - {e}")
    sys.exit(1)

try:
    import youtube_service
    print("  ✓ youtube_service.py")
except Exception as e:
    print(f"  ✗ youtube_service.py - {e}")
    sys.exit(1)

try:
    import app
    print("  ✓ app.py")
except Exception as e:
    print(f"  ✗ app.py - {e}")
    sys.exit(1)

# Test 3: Check Config class
print("\n3. Testing configuration...")
try:
    from config import Config
    
    # Check if required attributes exist
    required_attrs = [
        'SECRET_KEY',
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET',
        'SPOTIFY_REDIRECT_URI',
        'SPOTIFY_SCOPE',
        'YOUTUBE_CLIENT_ID',
        'YOUTUBE_CLIENT_SECRET',
        'YOUTUBE_REDIRECT_URI',
        'YOUTUBE_SCOPES',
        'YOUTUBE_API_SERVICE_NAME',
        'YOUTUBE_API_VERSION'
    ]
    
    for attr in required_attrs:
        if hasattr(Config, attr):
            print(f"  ✓ Config.{attr}")
        else:
            print(f"  ✗ Config.{attr} - Missing!")
            sys.exit(1)
    
    print("  All configuration attributes present!")
except Exception as e:
    print(f"  ✗ Configuration test failed: {e}")
    sys.exit(1)

# Test 4: Check Service classes
print("\n4. Testing service classes...")
try:
    from spotify_service import SpotifyService
    spotify = SpotifyService()
    print("  ✓ SpotifyService instantiated")
except Exception as e:
    print(f"  ✗ SpotifyService failed: {e}")
    sys.exit(1)

try:
    from youtube_service import YouTubeService
    youtube = YouTubeService()
    print("  ✓ YouTubeService instantiated")
except Exception as e:
    print(f"  ✗ YouTubeService failed: {e}")
    sys.exit(1)

# Test 5: Check Flask app
print("\n5. Testing Flask application...")
try:
    from app import app as flask_app
    
    # Check if required routes exist
    routes = [
        '/',
        '/connect/spotify',
        '/spotify/callback',
        '/connect/youtube',
        '/youtube/callback',
        '/playlists',
        '/convert',
        '/disconnect/spotify',
        '/disconnect/youtube'
    ]
    
    app_routes = [rule.rule for rule in flask_app.url_map.iter_rules()]
    
    for route in routes:
        if route in app_routes:
            print(f"  ✓ Route: {route}")
        else:
            print(f"  ✗ Route missing: {route}")
            sys.exit(1)
    
    print("  All routes registered!")
except Exception as e:
    print(f"  ✗ Flask app test failed: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("✓ All tests passed successfully!")
print("=" * 50)
print("\nThe application structure is correct and ready to use.")
print("\nNext steps:")
print("1. Set up Spotify API credentials at: https://developer.spotify.com/dashboard")
print("2. Set up YouTube API credentials at: https://console.cloud.google.com/")
print("3. Copy .env.example to .env and add your credentials")
print("4. Install dependencies: pip install -r requirements.txt")
print("5. Run the app: python app.py")
