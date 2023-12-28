from moviepy.editor import AudioFileClip

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
