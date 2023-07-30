# My Awesome Spotify Liked Tracks Playlist Generator

[![License](https://img.shields.io/badge/License-MIT-cyan.svg)](https://opensource.org/licenses/MIT)

A web application that generates a Spotify playlist containing all your liked tracks. I.e. it converts your Spotify Liked Songs into a playlist.

## Features

- Authenticate with Spotify using OAuth 2.0.
- Fetch all your liked tracks from Spotify.
- Create a new public playlist named "LikedTracks" on your Spotify account.
- Add all your liked tracks to the playlist.
- Pagination support for fetching large numbers of liked tracks.

## Prerequisites

- Python 3.7+
- Spotify Developer Account

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/your-username/spotify-liked-tracks-playlist-generator.git
   cd spotify-liked-tracks-playlist-generator
   ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your Spotify Developer credentials:

    Go to the Spotify Developer Dashboard and create a new application.
    Add http://localhost:8888/callback as a Redirect URI in your Spotify application settings.
    Copy your Client ID and Client Secret and update config.example.py with these values. Then rename config.example.py to config.py.

4. Run the script:
    ```bash
    py index.py
    ```
    Follow the link displayed in the console to authenticate with your Spotify account.

## Contributing
Contributions are welcome! Just fork it, create a new feature branch and open a pull request.

## License
This project is licensed under the MIT License.