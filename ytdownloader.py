#!/bin/python
from pytube import Playlist, YouTube
from alive_progress import alive_bar
import os

def download_playlist(url, output_path):
    try:
        print("Playlist Detected!\n")
        playlist = Playlist(url)
        total_videos = len(playlist.video_urls)
        print(f"Total videos in playlist: {total_videos}")
        
        with alive_bar(total=total_videos, title="Downloading playlist", bar='filling') as bar:
            for video_url in playlist.video_urls:
                download_video(video_url, output_path)
                bar()
        
        print("Playlist download successful!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def download_video(url, output_path):
    try:
        print("Processing Video...")
        yt = YouTube(url)
        stream = yt.streams.filter(res="720p", progressive=True, file_extension='mp4').first()
        
        if stream is None:
            print(f"No suitable stream found for {yt.title}")
            return
        
        print(f"Downloading {yt.title}...")        
        # Create directory if it doesn't exist
        if not output_path:
            output_path = "."  # Default to current directory
        
        os.makedirs(output_path, exist_ok=True)
        stream.download(output_path=output_path, filename=yt.title)
        file_path = os.path.join(output_path, f"{yt.title}.mp4")
           
        print(f"Downloaded: {yt.title} \n")
    except Exception as e:
        print(f"Error occurred: {str(e)}\n")        

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    output_path = input("Enter the output directory to save the videos: ").strip()
    print("Detecting URL Type...\n")
    if 'playlist' in url.lower():
        download_playlist(url, output_path)
    else:
        download_video(url, output_path)
