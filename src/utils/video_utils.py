import random
from moviepy.editor import clips_array, vfx, VideoFileClip

def combine_clips_top_bottom(clip1, clip2):
    """
    Combines two video clips into one, placing one on top of the other.
    :param clip1: moviepy.editor.VideoFileClip, the first video clip
    :param clip2: moviepy.editor.VideoFileClip, the second video clip
    :return: moviepy.editor.VideoFileClip, the combined video clip
    """
    # Ensure both clips are of the same width for a uniform look
    clip1 = clip1.fx(vfx.resize, width=clip2.size[0])

    # Combine the clips in a vertical array (one on top of the other)
    combined_clip = clips_array([[clip1], [clip2]])

    return combined_clip

def combine_clips_left_right(clip1, clip2):
    """
    Combines two video clips into one, placing one on top of the other.
    :param clip1: moviepy.editor.VideoFileClip, the first video clip
    :param clip2: moviepy.editor.VideoFileClip, the second video clip
    :return: moviepy.editor.VideoFileClip, the combined video clip
    """
    # Ensure both clips are of the same width for a uniform look
    clip1 = clip1.fx(vfx.resize, width=clip2.size[0])

    # Combine the clips in a vertical array (one on top of the other)
    combined_clip = clips_array([[clip1, clip2]])

    return combined_clip


import random

def match_and_combine_clips(top_clips, bottom_clips):
    combined_clips = {}

    for top_filename, top_clip in top_clips.items():
        # Choose a random bottom filename and corresponding clip
        bottom_filename, bottom_clip = random.choice(list(bottom_clips.items()))

        # Combine the top clip with the chosen bottom clip
        combined_clip = combine_clips_top_bottom(top_clip, bottom_clip)

        # Create a new filename for the combined clip
        combined_filename = f"{top_filename}_and_{bottom_filename}"

        # Add the combined clip to the dictionary
        combined_clips[combined_filename] = combined_clip

    return combined_clips

def convert_mp4_to_gif(input_file, output_file):
    """
    Convert an MP4 file to GIF format.

    :param input_file: Path to the input MP4 file.
    :param output_file: Path where the output GIF should be saved.
    """
    clip = VideoFileClip(input_file)
    clip = clip.set_duration(clip.duration - 1)
    clip.write_gif(output_file, program='ffmpeg', fps=12)