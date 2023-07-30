import logging
import spotipy
import config
from flask import Flask, request
from spotipy.oauth2 import SpotifyOAuth
import threading

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Spotify credentials
client_id = config.CLIENT_ID
client_secret = config.CLIENT_SECRET
redirect_uri = config.REDIRECT_URI
scope = 'user-library-read playlist-modify-public'

# Create a SpotifyOAuth instance to handle authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

def create_playlist_with_liked_tracks():
    logger.info('Starting...')
    count_added_tracks = 0
    liked_tracks_limit = 50
  
    try:
        # Get the user's liked tracks (max limit is 50)
        liked_tracks = sp.current_user_saved_tracks(limit=liked_tracks_limit)

        # Create a new playlist
        playlist_name = 'LikedTracks'
        playlist_description = 'A playlist containing all my liked tracks on Spotify.'
        playlist = sp.user_playlist_create(user=sp.me()['id'], name=playlist_name, public=True, description=playlist_description)

        while liked_tracks['items']:
            # Add liked tracks to the newly created playlist
            track_uris = [track['track']['uri'] for track in liked_tracks['items']]
            sp.user_playlist_add_tracks(user=sp.me()['id'], playlist_id=playlist['id'], tracks=track_uris)

            count_added_tracks += len(track_uris)

            if liked_tracks['next']:
                logger.info('Fetching more liked tracks...')
                liked_tracks = sp.next(liked_tracks)
            else:
                break

        logger.info(f"Playlist '{playlist_name}' created with all {count_added_tracks} liked tracks.")

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        
# Create an endpoint to do OAuth flow
@app.route('/callback')
def callback():
    global sp

    try:
        auth_code = request.args.get('code')
        logger.info(f"Received authorization code: {auth_code}")
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
