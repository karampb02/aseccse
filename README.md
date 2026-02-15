# Spotify to YouTube Playlist Converter

A Flask web application that converts your Spotify playlists to YouTube playlists. The app bridges Spotify and YouTube APIs to automatically search for songs and create matching playlists.

## Features

- 🎵 Connect to your Spotify account
- 📺 Connect to your YouTube account  
- 📋 View all your Spotify playlists
- 🔄 Convert entire playlists with one click
- 🔍 Automatically searches for songs on YouTube
- ✅ Creates YouTube playlists with found videos
- 📊 Reports conversion statistics and failed songs

## Prerequisites

Before running this application, you need to set up API credentials for both Spotify and YouTube:

### Spotify API Setup

1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click "Create an App"
4. Fill in the app name and description
5. Once created, you'll see your **Client ID** and **Client Secret**
6. Click "Edit Settings" and add `http://localhost:5000/spotify/callback` to Redirect URIs
7. Save your settings

### YouTube API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**:
   - Go to "APIs & Services" > "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Create OAuth 2.0 credentials:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add `http://localhost:5000/youtube/callback` to Authorized redirect URIs
   - Save and copy your **Client ID** and **Client Secret**

## Installation

1. Clone the repository:
```bash
git clone https://github.com/karampb02/aseccse.git
cd aseccse
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

5. Edit `.env` and add your API credentials:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
SPOTIFY_REDIRECT_URI=http://localhost:5000/spotify/callback

YOUTUBE_CLIENT_ID=your_youtube_client_id
YOUTUBE_CLIENT_SECRET=your_youtube_client_secret
YOUTUBE_REDIRECT_URI=http://localhost:5000/youtube/callback

FLASK_SECRET_KEY=your_random_secret_key_here
FLASK_ENV=development
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Follow the steps in the web interface:
   - Click "Connect Spotify" and authorize the app
   - Click "Connect YouTube" and authorize the app
   - Click "Load My Playlists" to see your Spotify playlists
   - Click "Convert" on any playlist to create it on YouTube
   - Wait for the conversion to complete (may take several minutes for large playlists)
   - Click the link to view your new YouTube playlist

## How It Works

### The Flow

1. **Authentication**: User authenticates with both Spotify and YouTube using OAuth 2.0
2. **Fetch Playlists**: App retrieves user's Spotify playlists
3. **Select Playlist**: User selects a playlist to convert
4. **Extract Songs**: App fetches all songs from the selected Spotify playlist (Artist + Track Name)
5. **Search & Match**: For each song, app searches YouTube for matching videos
6. **Create Playlist**: App creates a new YouTube playlist
7. **Add Videos**: App adds found videos to the new playlist

### The Search Algorithm

The matching algorithm works by:
1. Getting song data from Spotify in format: "Artist - Track Name"
2. Searching YouTube with query: "Artist Track Name"
3. Selecting the first video result (usually the official video or lyric video)
4. Extracting the video ID
5. Adding the video to the YouTube playlist

### API Quota Considerations

**Important**: YouTube has strict daily API quotas (default: 10,000 units per day)
- Each search costs 100 units
- Each playlist insert costs 50 units
- A 100-song playlist uses approximately 15,000 units (exceeds daily limit)

**Solutions**:
- Convert smaller playlists (under 50 songs recommended)
- Request a quota increase from Google Cloud Console
- Split large playlists into smaller ones

## Project Structure

```
aseccse/
├── app.py                  # Main Flask application
├── config.py              # Configuration settings
├── spotify_service.py     # Spotify API integration
├── youtube_service.py     # YouTube API integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── templates/
│   └── index.html       # Web interface
└── README.md            # This file
```

## Tech Stack

- **Backend**: Python 3.x + Flask
- **Spotify API**: spotipy library
- **YouTube API**: google-api-python-client
- **Authentication**: OAuth 2.0
- **Frontend**: HTML + Tailwind CSS + Vanilla JavaScript

## Troubleshooting

### "Not authenticated" errors
- Make sure you've connected both Spotify and YouTube accounts
- Try disconnecting and reconnecting if issues persist

### Songs not found
- Some songs may not be available on YouTube
- The search algorithm picks the first result, which may not always be accurate
- Consider manually adding missing songs to the YouTube playlist

### API quota exceeded
- This means you've hit YouTube's daily API limit
- Wait 24 hours for the quota to reset
- Request a quota increase from Google Cloud Console

### OAuth errors
- Verify your redirect URIs match exactly in both the API console and `.env` file
- Check that your client IDs and secrets are correct
- Ensure APIs are enabled in respective developer consoles

## Security Notes

- Never commit your `.env` file or API credentials to version control
- Keep your `FLASK_SECRET_KEY` secure and random
- In production, use environment variables or secure secret management
- Store credentials securely (not in sessions for production apps)

## Limitations

- YouTube search may not always find the exact song version from Spotify
- Some songs may be region-restricted on YouTube
- API quotas limit the number of playlists you can convert per day
- Requires manual authentication for each session (tokens not persisted)

## Future Enhancements

- Persistent credential storage
- Batch processing with retry logic
- Better search matching (using additional metadata)
- Progress bar during conversion
- Playlist comparison and updates
- Support for other platforms (Apple Music, SoundCloud)

## License

This project is provided as-is for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Built following the architecture described in the problem statement
- Uses official Spotify and YouTube APIs
- Inspired by the need to bridge music platforms
