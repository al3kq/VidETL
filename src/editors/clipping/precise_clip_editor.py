from base_clip_editor import BaseClipEditor

class PreciseClipEditor(BaseClipEditor):
    def __init__(self, video_path, start_time, end_time):
        super().__init__(video_path)
        self.start_time = start_time
        self.end_time = end_time

    def edit(self):
        """
        Extracts a specific clip from the video based on start and end times.
        """
        # Load the video file
        self.load_video()

        # Validate the time range
        if self.start_time < 0 or self.end_time > self.video.duration:
            raise ValueError("Invalid start or end time for the clip.")

        # Extract the specified subclip
        clip = self.video.subclip(self.start_time, self.end_time)

        return clip
