# class VideoWriter:
#     __init__(self, ):
""" Saves a list of clips with unique ids
    input: dictionary of clips
    output: list of video clips
"""
import time
def save_video_files(clips, out_dir):
    for filename, clip in clips.items():
        unique_id = int(time.time())
        output_filename = f"{out_dir}/{filename}_{unique_id}.mp4"
        clip.write_videofile(output_filename, bitrate='8000k', preset='slower', codec="libx264", fps=24)