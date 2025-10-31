import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from googleapiclient.discovery import build
import yt_dlp
import os
import time
import re

# --- CONFIGURATION (UPDATE THESE VALUES) ---
# IMPORTANT: Replace these with your actual API keys and secrets.
YOUTUBE_API_KEY = "Youtube_API_Key_Here"
SPOTIPY_CLIENT_ID = "spotipy_client_id_here"
SPOTIPY_CLIENT_SECRET = "spotipy_client_secret_here"
# ---------------------------------------------

def sanitize_filename(name):
    """Removes special characters to create a valid filename."""
    # Remove characters that are illegal in file paths
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Truncate to a reasonable length
    return name[:150]

def get_downloaded_filenames(download_dir='.'):
    """Returns a set of sanitized filenames (without extension) that already exist."""
    downloaded_files = set()
    try:
        # Check all files in the current directory (or specified download_dir)
        for filename in os.listdir(download_dir):
            if filename.endswith(".mp3"):
                # Remove the .mp3 extension
                base_name = os.path.splitext(filename)[0]
                downloaded_files.add(base_name)
    except FileNotFoundError:
        print(f"Warning: Download directory '{download_dir}' not found.")
    return downloaded_files

def get_track_list(playlist_uri):
    """Fetches all tracks from a given Spotify playlist URI."""
    print("Connecting to Spotify...")
    try:
        auth_manager = SpotifyClientCredentials(
            client_id=SPOTIPY_CLIENT_ID, 
            client_secret=SPOTIPY_CLIENT_SECRET
        )
        sp = spotipy.Spotify(auth_manager=auth_manager)
    except Exception as e:
        print(f"Error initializing Spotify client: {e}")
        return []

    # Extract playlist ID from URI or URL
    if 'playlist' in playlist_uri:
        # Get the segment after the last colon or slash (which includes the ID and potentially query params)
        last_segment = playlist_uri.split(':')[-1].split('/')[-1]
        
        # Strip off any trailing query parameters (like '?si=...')
        if '?' in last_segment:
            playlist_id = last_segment.split('?')[0]
        else:
            playlist_id = last_segment
    else:
        print("Invalid Spotify playlist URI or URL.")
        return []

    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    
    # Paginate through results if the playlist has more than 100 tracks
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    track_data = []
    for item in tracks:
        track = item.get('track')
        if track:
            artist_names = ", ".join([artist['name'] for artist in track['artists']])
            track_name = track['name']
            track_data.append({
                'name': track_name,
                'artist': artist_names,
                'search_query': f"{track_name} {artist_names} audio"
            })
    
    print(f"Found {len(track_data)} tracks in the playlist.")
    return track_data

def search_youtube(query):
    """Searches YouTube for the best matching video and returns its ID."""
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=1
        )
        response = request.execute()
        
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except Exception as e:
        print(f"Error searching YouTube for '{query}': {e}")
        return None

def download_audio(youtube_url, filename):
    """Downloads audio from YouTube URL and saves it as an MP3."""
    output_path = f"{filename}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': filename,
        'sleep_interval_requests': 1.0, # Slow down requests slightly
        'no_warnings': True,
        'ignoreerrors': True,
    }
    
    try:
        # yt-dlp requires ffprobe and ffmpeg in PATH or the current directory for post-processing
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Add a slight delay to avoid rate-limiting
            time.sleep(2) 
            info_dict = ydl.extract_info(youtube_url, download=True)
            return True
    except yt_dlp.DownloadError as e:
        print(f"YT-DLP Download Error: {e}")
        print("HINT: Ensure FFmpeg (ffmpeg.exe and ffprobe.exe) is in the script directory or system PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        return False

def main():
    """Main function to run the downloader."""
    print("\n--- Spotify Playlist to MP3 Downloader ---")
    
    # 1. Get playlist URI
    playlist_uri = input("Enter the Spotify Playlist URL or URI: ").strip()
    if not playlist_uri:
        print("No URI provided. Exiting.")
        return

    # 2. Get track list
    tracks = get_track_list(playlist_uri)
    if not tracks:
        print("Could not retrieve tracks. Check your playlist URI and API keys.")
        return

    # 3. Get list of already downloaded songs
    downloaded_files = get_downloaded_filenames()
    print(f"Found {len(downloaded_files)} existing MP3 files to skip.")

    # 4. Process and download each track
    for i, track in enumerate(tracks, 1):
        full_name = f"{track['artist']} - {track['name']}"
        sanitized_name = sanitize_filename(full_name)
        
        # --- NEW SKIP LOGIC ---
        if sanitized_name in downloaded_files:
            print(f"\n[{i}/{len(tracks)}] SKIP: '{full_name}' already exists.")
            continue
        # ----------------------

        print(f"\n[{i}/{len(tracks)}] Processing: {full_name}")

        # Search YouTube
        youtube_url = search_youtube(track['search_query'])

        if youtube_url:
            print(f"  -> Found YouTube match: {youtube_url}")
            # Download and convert
            success = download_audio(youtube_url, sanitized_name)
            if success:
                print(f"  -> Successfully downloaded and saved as '{sanitized_name}.mp3'")
            else:
                print(f"  -> Failed to download/convert '{full_name}'. Check FFmpeg installation.")
        else:
            print(f"  -> No suitable YouTube video found for '{full_name}'. Skipping.")

    print("\n--- Download process complete! ---")

if __name__ == "__main__":
    # Ensure API keys are set before running
    if "YOUR_YOUTUBE_API_KEY_HERE" in YOUTUBE_API_KEY or "YOUR_SPOTIPY_CLIENT_ID_HERE" in SPOTIPY_CLIENT_ID:
        # This check is now redundant since the user provided the keys, but we keep it for safety if they were still placeholders.
        print("\nFATAL ERROR: Please update YOUTUBE_API_KEY, SPOTIPY_CLIENT_ID, and SPOTIPY_CLIENT_SECRET in the script.")
    else:
        main()
