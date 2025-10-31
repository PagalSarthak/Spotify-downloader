# 🎶 Spotify Playlist to MP3 Downloader

A robust Python script designed to automatically download every track from a specified Spotify playlist and convert it to a high-quality MP3 file. It uses the Spotify API to read the tracklist and the YouTube Data API/yt-dlp for finding and downloading the best matching audio source.

# ✨ Features

Batch Processing: Downloads all tracks from any public Spotify playlist.

Smart Skipping: Automatically checks for and skips tracks that have already been downloaded to prevent redundant work and save API quota.

Robust Input: Handles both clean Spotify URIs and full web URLs (including sharing links with query parameters).

MP3 Conversion: Uses FFmpeg for reliable audio extraction and conversion to a standard MP3 format.

# ⚙️ Prerequisites

Before running the script, you must have the following installed and configured:

_1. Python 3.x_

Ensure you have Python 3.x installed on your system.

_2. FFmpeg_

This is crucial for converting the downloaded YouTube audio stream into the final MP3 file.

Download FFmpeg from their [official website.](https://www.ffmpeg.org/)

Extract the ZIP file and locate the bin folder.

Copy the two executable files, ffmpeg.exe and ffprobe.exe, into the same directory where your main.py script is located.

_3. API Keys_

You need credentials for both Spotify and Google/YouTube. These keys are already configured in the provided main.py script, but you should know where they come from if you need to generate new ones.

    YOUTUBE_API_KEY = "Youtube_API_Key_Here"
    SPOTIPY_CLIENT_ID = "spotipy_client_id_here"
    SPOTIPY_CLIENT_SECRET = "spotipy_client_secret_here"```

# 🚀 Setup and Installation

_Step 1: Install Python Dependencies_

Open your terminal or command prompt in the directory containing main.py and run the following command to install the necessary Python libraries:
```
py -m pip install spotipy google-api-python-client yt-dlp pyinstaller
```

_Step 2: Configure API Keys_

You must edit the main.py file and replace the placeholder values for these three variables with your own credentials:

```
# --- CONFIGURATION (UPDATE THESE VALUES) ---
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY_HERE"
SPOTIPY_CLIENT_ID = "YOUR_SPOTIPY_CLIENT_ID_HERE"
SPOTIPY_CLIENT_SECRET = "YOUR_SPOTIPY_CLIENT_SECRET_HERE"
# ---------------------------------------------
 ```

# ▶️ Usage

Running the Python Script

Ensure you have completed the prerequisites (Python dependencies and FFmpeg executables in the script directory).

Run the script from your terminal:

```
python main.py 
```


The script will prompt you to ```"Enter the Spotify Playlist URL or URI:"```

Paste the full URL (e.g., https://open.spotify.com/playlist/YOUR_ID...) and press Enter.

The script will process each track, search YouTube, download, and convert the audio.


# Creating a Standalone Executable (.exe)

You can compile the script into a single executable file using PyInstaller (which you installed in Step 1):

Run the PyInstaller command in your terminal:

```
# Use 'py -m pyinstaller' if the 'pyinstaller' command is not recognized
py -m pyinstaller --onefile main.py
```

The final executable will be located in the newly created dist folder (e.g., dist/main.exe).

Note for sharing: If you share the main.exe file, the recipient must still place ffmpeg.exe and ffprobe.exe in the same folder as the executable for the conversion process to work.
