import random
from moviepy.editor import VideoFileClip, AudioFileClip

def select_random_clip(video_path, start_time, duration):
    """
    Extracts a random 30-second clip from the video, starting any time between the given start_time and the end of the video.

    :param video_path: str, path to the video file
    :param start_time: int or float, start time to begin considering clips in seconds
    :return: moviepy.editor.VideoFileClip object, the extracted video clip
    """
    # Load the video file
    video = VideoFileClip(video_path)

    # Calculate the latest possible start time for a 30-second clip
    max_clip_start_time = video.duration - duration

    # Ensure start_time is not later than max_clip_start_time
    if start_time > max_clip_start_time:
        raise ValueError("Start time is too late in the video to extract a 30-second clip.")

    # Generate a random start time for the clip within the feasible range
    random_start_time = random.uniform(start_time, max_clip_start_time)

    # Extract the 30-second subclip
    clip = video.subclip(random_start_time, random_start_time + duration)

    return clip


def reformat_video(clip):
    """
    Reformats a video clip to a 9:16 aspect ratio for TikTok.

    :param clip: moviepy.editor.VideoFileClip, the video clip to be reformatted
    :return: moviepy.editor.VideoFileClip, the reformatted video clip
    """
    original_width, original_height = clip.size

    # Desired aspect ratio for TikTok (9:16)
    aspect_ratio = 9 / 16

    # Calculate the target width based on the original height and desired aspect ratio
    target_width = original_height * aspect_ratio

    # If the target width is less than the original, we crop horizontally
    if target_width <= original_width:
        # Calculate the cropping area
        crop_x_start = (original_width - target_width) / 2
        cropped_clip = clip.crop(x1=crop_x_start, y1=0, width=target_width, height=original_height)
    else:
        # If the target width is more than the original, we crop vertically
        target_height = original_width / aspect_ratio
        crop_y_start = (original_height - target_height) / 2
        cropped_clip = clip.crop(x1=0, y1=crop_y_start, width=original_width, height=target_height)

    return cropped_clip


def reformat_video_cut_bottom(clip):
    """
    Reformats a video clip to an 8:9 aspect ratio and cuts off the bottom 5%.

    :param clip: moviepy.editor.VideoFileClip, the video clip to be reformatted
    :return: moviepy.editor.VideoFileClip, the reformatted video clip
    """
    original_width, original_height = clip.size

    # Desired aspect ratio
    aspect_ratio = 8 / 9

    # Calculate the target height based on the original width and desired aspect ratio
    target_height = original_width * aspect_ratio

    # Adjust the target height to remove the bottom 5%
    cut_off_height = target_height * 0.05  # 5% of the target height
    target_height_adjusted = target_height - cut_off_height

    # If the target height is less than the original, we crop vertically
    if target_height_adjusted <= original_height:
        # Calculate the cropping area
        crop_y_start = (original_height - target_height_adjusted) / 2
        cropped_clip = clip.crop(y1=crop_y_start, y2=crop_y_start + target_height_adjusted)
    else:
        # If the target height is more than the original, we crop horizontally
        # and adjust to remove the bottom 5%
        target_width = original_height / aspect_ratio
        crop_x_start = (original_width - target_width) / 2
        cropped_clip = clip.crop(x1=crop_x_start, x2=crop_x_start + target_width, y1=0, y2=original_height - cut_off_height)

    return cropped_clip


from moviepy.editor import VideoFileClip

def extract_audio_from_video(clip, output_audio_file_path):
    """
    Extracts the audio from a video file and saves it as an audio file.

    :param video_file_path: str, path to the video file
    :param output_audio_file_path: str, path where the extracted audio file will be saved
    """
    audio_clip = clip.audio
    audio_clip.write_audiofile(output_audio_file_path)
    audio_clip.close()


import requests
import json
import whisper_timestamped as whisper

def generate_captions(audio_file_path):
    audio = whisper.load_audio(audio_file_path)
    model = whisper.load_model("tiny", device="cpu")
    result = whisper.transcribe(model, audio, language="en")
    captions = json.dumps(result, indent = 2, ensure_ascii = False)
    return result


from moviepy.editor import CompositeVideoClip, TextClip

def add_captions_to_clip(clip, json_data, caption_font='Arial', caption_fontsize=24, caption_color='white'):
    """
    Adds synchronized captions to a video clip based on JSON data.

    :param clip: moviepy.editor.VideoFileClip, the video clip to add captions to
    :param json_data: dict, parsed JSON data containing captions and timestamps
    :param caption_font: str, the font of the caption
    :param caption_fontsize: int, the font size of the caption
    :param caption_color: str, the color of the caption
    :return: moviepy.editor.VideoFileClip, the video clip with captions
    """
    clips = [clip]  # Start with the original clip

    for segment in json_data['segments']:
        for word_info in segment['words']:
            word = word_info['text']
            start_time = word_info['start']
            end_time = word_info['end']

            # Create a TextClip for each word
            txt_clip = TextClip(word, fontsize=caption_fontsize, font=caption_font, color=caption_color)
            txt_clip = txt_clip.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

            outline_txt = TextClip(word, fontsize=caption_fontsize+2, font=caption_font, color="black")
            outline_txt_clip = outline_txt.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

            # Add the text clip to the list of clips
            clips.append(outline_txt_clip)
            clips.append(txt_clip)


    # Composite all clips (original and text clips) together
    video_with_captions = CompositeVideoClip(clips)

    return video_with_captions

def add_audio(clip, audio_path):
    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.set_duration(clip.duration)
    clip = clip.set_audio(audio_clip)
    return clip

from moviepy.editor import clips_array, vfx

def combine_clips(clip1, clip2):
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


import time, os

def main():
    num_clips = 1  # Specify the number of clips you want to generate

    for i in range(num_clips):
        unique_id = int(time.time())  # Generate a unique timestamp ID

        # Clip 1 processing
        start_time1 = 0
        print(f"Selecting Random Snippet for Clip {i+1}")
        clip1 = select_random_clip("american_dad_funny.mp4", start_time1, 23)
        clip1 = reformat_video_cut_bottom(clip1)
        audio_filename = f"audio_{unique_id}.wav"
        print("Extracting Audio")
        extract_audio_from_video(clip1, audio_filename)
        print("Generating Captions")
        captions = generate_captions(audio_filename)
        print("Adding Captions to Snippet")
        clip1 = add_captions_to_clip(clip1, captions)
        # clip1 = clip1.without_audio()

        clip1 = add_audio(clip1, "voice.mp3")

        # delete audio file
        if os.path.exists(audio_filename):
            os.remove(audio_filename)

        # # Clip 2 processing
        # start_time2 = 60
        # print(f"Selecting Second Snippet for Clip {i+1}")
        # clip2 = select_random_clip("fortnite.mp4", start_time2, 25)
        # clip2 = reformat_video_cut_bottom(clip2)
        # clip2 = clip2.without_audio()

        # # Combine clips
        # print(f"Combining Snippets for Clip {i+1}")
        # final_video = combine_clips(clip1, clip2)
        output_filename = f"final_output_{unique_id}.mp4"
        # final_video.write_videofile(output_filename, codec="libx264", fps=24)
        clip1.write_videofile(output_filename, codec="libx264", fps=24)

        print(f"Clip {i+1} processed and saved as {output_filename}")


if __name__ == "__main__":
    main()
