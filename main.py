import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth



def create_spotify_client():
    SPOTIFY_CLIENT_ID = '343c6c4456c8495294d0a92599966706'
    SPOTIFY_CLIENT_SECRET = '89cb9cc67d9e4005a1f34e5d5274e0dc'
    SPOTIFY_REDIRECT_URI = 'http://localhost:8080'
    
    SCOPE = "user-library-read playlist-modify-public"
    
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id = SPOTIFY_CLIENT_ID,
        client_secret = SPOTIFY_CLIENT_SECRET,
        redirect_uri= SPOTIFY_REDIRECT_URI,
        scope=SCOPE
        ))

def get_seed_tracks(client):
    seed_track_ids = []
    for i in range(3):
        artist = input(f"Enter the artst: ")
        track_name = input(f"Enter the track name: ")
        
        search_result = client.search(q = f'artist:{artist} track:{track_name}')
        trackid = search_result['tracks']['items'][0]['id']
        seed_track_ids.append(trackid)
        
    return seed_track_ids

def create_curated_playlist(client, tracks):
    reccommendations = client.recommendations(seed_tracks=tracks, limit=50)
    track_uris = [track['uri'] for track in reccommendations['tracks']]
    
    user_id = client.current_user()['id']
    playlist_name = "Custom playlist"
    playlist = client.user_playlist_create(user_id,playlist_name, public = True)
    
    client.playlist_add_items(playlist['id'], track_uris)

client = create_spotify_client()
tracks_to_create_playlist = get_seed_tracks(client)
create_curated_playlist(client,tracks_to_create_playlist)
print('Playlist created')