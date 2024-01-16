from moviepy.editor import AudioFileClip
import json

def add_audio(clip, audio_path):
    """
    Adds an audio track to a given video clip.

    :param clip: moviepy.editor.VideoFileClip, the video clip to add audio to
    :param audio_path: str, path to the audio file
    :return: moviepy.editor.VideoFileClip, the video clip with added audio
    """
    audio_clip = AudioFileClip(audio_path)
    audio_clip = audio_clip.set_duration(clip.duration)
    clip = clip.set_audio(audio_clip)
    return clip


def extract_audio(clip, output_audio_file_path):
    """
    Extracts the audio from a video file and saves it as an audio file.

    :param video_file_path: str, path to the video file
    :param output_audio_file_path: str, path where the extracted audio file will be saved
    """
    audio_clip = clip.audio
    audio_clip.write_audiofile(output_audio_file_path)
    audio_clip.close()


