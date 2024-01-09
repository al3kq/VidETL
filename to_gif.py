import os
from .src.utils.video_utils import convert_mp4_to_gif

def convert_directory_mp4s_to_gifs(directory):
    """
    Convert all MP4 files starting with 'gif' in the given directory to GIFs.

    :param directory: Path to the directory containing MP4 files.
    """
    for filename in os.listdir(directory):
        if filename.startswith("gif") and filename.endswith(".mp4"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, filename.replace(".mp4", ".gif"))
            convert_mp4_to_gif(input_file, output_file)
            print(f"Converted {input_file} to {output_file}")

# Example usage
convert_directory_mp4s_to_gifs("output")