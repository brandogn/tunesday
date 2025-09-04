import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

DEFAULT_PLAYLIST_ID = "5VAWBjNvITrvEFSYwgq5iK"

def get_spotify_client_token():
    """
    Get Spotify access token using client credentials flow
    """
    url = "https://accounts.spotify.com/api/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": os.getenv("SPOTIFY_CLIENT_ID"),
        "client_secret": os.getenv("SPOTIFY_CLIENT_SECRET")
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def get_spotify_playlist(playlist_id: str, access_token: str):
    """
    Get tracks from a playlist with enhanced metadata
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "fields": "name,tracks(items(track(id,name,artists(name),album(name,release_date),duration_ms,external_ids(isrc)),added_at))"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        print(response.json().get('name', ""))
        return response.json()
    else:
        raise Exception(f"Failed to get playlist tracks: {response.status_code} - {response.text}")

def parse_spotify_playlist(playlist: dict):
    """
    Parse tracks from a playlist and return enhanced track data
    """
    parased_tracks = []
    
    name = playlist.get('name', '')
    items = playlist.get('tracks', {}).get('items', [])
    
    for index, item in enumerate(items, 1):
        track = item.get('track', {})
        album = track.get('album', {})
        artists = track.get('artists', [])
        
        track_data = {
            'position': index,
            'artists': ", ".join(artist.get('name', '') for artist in artists),
            'name': track.get('name', ''),
            'album': album.get('name', ''),
            'release_date': album.get('release_date', ''),
            'duration_formatted': format_duration(track.get('duration_ms', 0)),
            'spotify_url': f"https://open.spotify.com/track/{track.get('id', '')}" if track.get('id') else "",
            'isrc': track.get('external_ids', {}).get('isrc', ''),
            'added_at': item.get('added_at', '')
        }
        parased_tracks.append(track_data)
    return {
        'name': name,
        'tracks': parased_tracks
    }

def format_duration(duration_ms):
    """
    Convert milliseconds to MM:SS format
    """
    if not duration_ms:
        return "0:00"
    
    seconds = duration_ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"

def save_playlist_data(playlist_data, date_str=None):
    """
    Save playlist data to JSON file
    """
    if not date_str:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    filename = f"data/playlist_{date_str}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(playlist_data, f, indent=2, ensure_ascii=False)
    
    return filename

def fetch_and_save_playlist(playlist_id=DEFAULT_PLAYLIST_ID):
    """
    Fetch playlist data and save it with current date
    """
    load_dotenv()
    
    try:
        # Get access token
        token_response = get_spotify_client_token()
        access_token = token_response['access_token']
        
        # Fetch playlist tracks
        tracks_response = get_spotify_playlist(playlist_id, access_token)
        parsed_tracks = parse_spotify_playlist(tracks_response)
        
        # Create playlist data structure
        name = parsed_tracks.get('name', '')
        tracks = parsed_tracks.get('tracks', [])
        playlist_data = {
            'playlist_id': playlist_id,
            'playlist_url': f"https://open.spotify.com/playlist/{playlist_id}",
            'name': name,
            'date': datetime.now().strftime("%Y-%m-%d"),
            'timestamp': datetime.now().isoformat(),
            'total_tracks': len(tracks),
            'tracks': tracks
        }
        
        # Save to file
        filename = save_playlist_data(playlist_data)
        
        return {
            'success': True,
            'filename': filename,
            'total_tracks': len(tracks),
            'timestamp': playlist_data['timestamp']
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    result = fetch_and_save_playlist()
    if result['success']:
        print(f"Successfully saved playlist data to {result['filename']}")
        print(f"Total tracks: {result['total_tracks']}")
    else:
        print(f"Error: {result['error']}")
