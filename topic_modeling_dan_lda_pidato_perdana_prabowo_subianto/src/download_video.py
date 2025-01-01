import subprocess
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi


def get_youtube_video_id(url):
    if 'watch?v=' in url:  # Standard YouTube video URL
        video_id = url.split('v=')[1]
        return video_id
    elif 'youtube.com/live/' in url:  # YouTube live video URL
        video_id = url.split('/live/')[1]
        return video_id
    else:
        video_id = None
    return video_id

def download_video_audio(url, output_path="data/audios"):
    os.makedirs(output_path, exist_ok=True)

    # Modify output template to save as video ID
    output_template = os.path.join(output_path, "%(id)s.%(ext)s")

    # Check if the file already exists
    video_id = get_youtube_video_id(url)


    if video_id:
        existing_files = [f for f in os.listdir(output_path) if f.startswith(video_id)]
        if existing_files:
            print(f"File already exists: {existing_files[0]} - Skipping download.")
            return video_id


    command = [
        "yt-dlp",
        "-f", "bestaudio",  # Download audio only
        "-o", output_template,
        url,
    ]
    try:
        subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Audio downloaded successfully")
        
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while downloading Audio: {e}")
        raise
    
    return video_id
