from ..base_editor import BaseEditor
class PreciseClipEditor(BaseEditor):
    start_time: float
    end_time: float
    silent: bool = False

    def apply(self, video_clip):
        """
        Extracts a specific clip from the video based on start and end times.
        """

        if self.silent:
            video_clip = video_clip.without_audio()

        # Validate the time range
        if self.start_time < 0 or self.end_time > video_clip.duration:
            raise ValueError("Invalid start or end time for the clip.")

        # Extract the specified subclip
        clip = video_clip.subclip(self.start_time, self.end_time)

        return clip
