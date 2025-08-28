import os
import requests
from dotenv import load_dotenv

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
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def get_spotify_playlist_tracks(playlist_id: str, access_token: str):
    """
    Get tracks from a playlist
    """
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "fields": "items(track(id,name,artists(name),external_ids))" # alt: external_ids(isrc)
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get playlist tracks: {response.status_code} - {response.text}")

def parse_spotify_tracks(tracks: dict):
    """
    Parse tracks from a playlist and return a list of (artists, track name, url, isrc) tuples.
    Each tuple is (comma-separated artist names, track name, track url, ISRC code).
    """
    result = []
    for item in tracks.get('items', []):
        track = item.get('track', {})
        artists = track.get('artists', [])
        artist_names = ", ".join(artist.get('name', '') for artist in artists)
        track_name = track.get('name', '')
        track_id = track.get('id', '')
        track_url = f"https://open.spotify.com/track/{track_id}" if track_id else ""
        isrc = track.get('external_ids', {}).get('isrc', '')
        
        result.append((artist_names, track_name, track_url, isrc))
    return result

def convert_spotify_to_apple(tracks: list):
    """
    Convert Spotify tracks to Apple Music tracks
    """
    result = []
    for track in tracks:
        result.append(track)
    return result

if __name__ == "__main__":
    load_dotenv()

    SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    try:
        access_token = get_spotify_client_token()['access_token']
    except Exception as e:
        print(f"Error: {e}")
    
    
    test_playlist_id = "3cEYpjA9oz9GiPac4AsH4n"
    tracks = get_spotify_playlist_tracks(test_playlist_id, access_token)
    parsed_tracks = parse_spotify_tracks(tracks)

    print(parsed_tracks)

    # apple_tracks = convert_spotify_to_apple(parsed_tracks)
    # print(apple_tracks)

