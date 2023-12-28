from moviepy.editor import VideoFileClip

class BaseClipEditor:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = None

    def load_video(self):
        """
        Loads the video file into a MoviePy VideoFileClip object.
        """
        self.video = VideoFileClip(self.video_path)
