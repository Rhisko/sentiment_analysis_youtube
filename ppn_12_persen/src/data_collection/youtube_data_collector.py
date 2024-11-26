import os
import json
from googleapiclient.discovery import build
import yaml

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

def load_config():
    with open("config/config.yaml", "r") as file:
        return yaml.safe_load(file)

def get_video_comments(api_key, video_id, max_results):
    youtube = build("youtube", "v3", developerKey=api_key)
    comments = []
    next_page_token = None
    fetched_comments = 0

    while fetched_comments <= max_results:
        response = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=min(100, max_results - fetched_comments),  # YouTube API limits maxResults to 100
            textFormat="plainText",
            pageToken=next_page_token  # Include the next page token if available
        ).execute()

        # Extract comments from the response
        comments.extend([
            item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            for item in response["items"]
        ])
        
        fetched_comments += len(response["items"])
        next_page_token = response.get("nextPageToken")
        print(f"fecth command == {fetched_comments}")

        # Break if there are no more pages
        if not next_page_token:
            break

    return comments


