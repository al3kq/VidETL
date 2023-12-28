import random
from base_clip_editor import BaseClipEditor

class RandomClipEditor(BaseClipEditor):
    def __init__(self, video_path, start_time, duration):
        super().__init__(video_path)
        self.start_time = start_time
        self.duration = duration

    def edit(self):
        """
        Extracts a random clip from the video.
        """
        # Load the video file
        self.load_video()

        # Calculate the latest possible start time for the clip
        max_clip_start_time = self.video.duration - self.duration

        # Ensure start_time is not later than max_clip_start_time
        if self.start_time > max_clip_start_time:
            raise ValueError("Start time is too late in the video to extract the clip.")

        # Generate a random start time for the clip within the feasible range
        random_start_time = random.uniform(self.start_time, max_clip_start_time)

        # Extract the subclip
        clip = self.video.subclip(random_start_time, random_start_time + self.duration)

        return clip
