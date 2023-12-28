class AudioExtractor:
    def __init__(self, video_clip):
        self.video_clip = video_clip

    def extract_audio_from_video(self, output_audio_file_path):
        """
        Extracts the audio from a video file and saves it as an audio file.

        :param video_file_path: str, path to the video file
        :param output_audio_file_path: str, path where the extracted audio file will be saved
        """
        audio_clip = self.video_clip.audio
        audio_clip.write_audiofile(output_audio_file_path)
        audio_clip.close()
