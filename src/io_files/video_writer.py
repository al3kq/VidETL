# class VideoWriter:
#     __init__(self, ):
""" Saves a list of clips with unique ids
    input: dictionary of clips
    output: list of video clips
"""
import time
def save_video_files(clips, out_dir):
    print("save start")
    for filename, clip in clips.items():
        unique_id = int(time.time())
        output_filename = f"{out_dir}/test_output_filename.mp4"
        # output_filename = f"{out_dir}/{filename}_{unique_id}.mp4"
        clip.write_videofile(output_filename, bitrate='8000k', preset='slower', codec="libx264", audio_codec="acc", fps=24)
        print("done writing file")