import os
from moviepy.editor import VideoFileClip

""" Run Pipeline on dir
    input: directory string, pipeline to execute
    output: dictionary of filenames to video clips
"""
def execute_pipeline_from_dir(directory, pipeline):
    clips = {}
    for filename in os.listdir(directory):
        if filename.endswith(".mp4"):
            # Load the original video clip
            original_video = VideoFileClip(os.path.join(directory, filename))
            # Execute pipeline on video
            filename = filename.split(".mp4")[0]
            final_clipped_video = pipeline.execute(original_video)
            clips[filename] = final_clipped_video
    return clips
