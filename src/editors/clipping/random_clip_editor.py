import random
from .base_clip_editor import BaseClipEditor

class RandomClipEditor(BaseClipEditor):
    def __init__(self,  start_time, duration, silent = False):
        self.start_time = start_time
        self.duration = duration
        self.silent = silent

    def apply(self, video_clip):
        """
        Extracts a random clip from the video.
        """
        if self.silent:
            video_clip = video_clip.without_audio()
        # Calculate the latest possible start time for the clip
        max_clip_start_time = video_clip.duration - self.duration

        # Ensure start_time is not later than max_clip_start_time
        if self.start_time > max_clip_start_time:
            raise ValueError("Start time is too late in the video to extract the clip.")

        # Generate a random start time for the clip within the feasible range
        random_start_time = random.uniform(self.start_time, max_clip_start_time)

        # Extract the subclip
        clip = video_clip.subclip(random_start_time, random_start_time + self.duration)

        return clip
