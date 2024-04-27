import logging
import spotipy
import config
from flask import Flask, request
from spotipy.oauth2 import SpotifyOAuth
import threading
from colorlog import ColoredFormatter
from tqdm import tqdm

app = Flask(__name__)

def setup_logger():
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger = setup_logger()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=config.CLIENT_ID,
    client_secret=config.CLIENT_SECRET,
    redirect_uri=config.REDIRECT_URI,
    scope='user-library-read playlist-modify-public'
))

def find_or_create_playlist(playlist_name, playlist_description):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            return playlist
    return sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True, description=playlist_description)

def add_tracks_to_playlist(playlist, tracks):
    existing_tracks = sp.playlist_tracks(playlist['id'])
    existing_track_uris = {track['track']['uri'] for track in existing_tracks['items']}
    
    new_tracks = [track['track']['uri'] for track in tracks if track['track']['uri'] not in existing_track_uris]
    if new_tracks:
        sp.user_playlist_add_tracks(user=sp.me()['id'], playlist_id=playlist['id'], tracks=new_tracks)
        return len(new_tracks)
    return 0

def create_playlist_with_liked_tracks():
    count_added_tracks = 0
    liked_tracks_limit = 50
    liked_tracks = sp.current_user_saved_tracks(limit=liked_tracks_limit)
    playlist = find_or_create_playlist('LikedTracks', 'A playlist containing all my liked tracks on Spotify.')

    total_tracks = liked_tracks['total']
    with tqdm(total=total_tracks, desc="Adding tracks to playlist", unit="track") as pbar:
        while liked_tracks['items']:
            added_tracks_count = add_tracks_to_playlist(playlist, liked_tracks['items'])
            count_added_tracks += added_tracks_count
            pbar.update(len(liked_tracks['items']))

            if liked_tracks['next']:
                liked_tracks = sp.next(liked_tracks)
            else:
                break

    logger.info(f"Playlist 'LikedTracks' updated with {count_added_tracks} new liked tracks.")

@app.route('/callback')
def callback():
    try:
        auth_code = request.args.get('code')
        sp.auth_manager.get_access_token(auth_code)
        logger.info("Authentication successful!")
        return "Authentication successful! You can close this window."
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return "An error occurred. Please check the logs for details.", 500

if __name__ == "__main__":
    thread = threading.Thread(target=app.run, kwargs={'port': 8888})
    thread.start()
    create_playlist_with_liked_tracks()
    thread.join()
