from .base_clip_editor import BaseClipEditor

class PreciseClipEditor(BaseClipEditor):
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time

    def apply(self, video_clip):
        """
        Extracts a specific clip from the video based on start and end times.
        """

        # Validate the time range
        if self.start_time < 0 or self.end_time > video_clip.duration:
            raise ValueError("Invalid start or end time for the clip.")

        # Extract the specified subclip
        clip = video_clip.subclip(self.start_time, self.end_time)

        return clip
