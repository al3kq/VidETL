from .base_format_editor import BaseFormatEditor

class AspectRatioFormatter(BaseFormatEditor):
    def __init__(self, target_aspect_ratio):
        self.target_aspect_ratio = self._parse_aspect_ratio(target_aspect_ratio)

    def _parse_aspect_ratio(self, aspect_ratio):
        """
        Parses the aspect ratio string and returns a numerical ratio.
        Aspect ratio should be in the format 'width:height' (e.g., '9:16').
        """
        width, height = aspect_ratio.split(':')
        return float(width) / float(height)

    def apply_format(self, video_clip):
        """
        Reformats a video clip to the specified aspect ratio.

        :return: moviepy.editor.VideoFileClip, the reformatted video clip
        """
        original_width, original_height = video_clip.size

        # Calculate the target dimensions based on the desired aspect ratio
        target_width = original_height * self.target_aspect_ratio

        if target_width <= original_width:
            crop_x_start = (original_width - target_width) / 2
            cropped_clip = video_clip.crop(x1=crop_x_start, y1=0, width=target_width, height=original_height)
        else:
            target_height = original_width / self.target_aspect_ratio
            crop_y_start = (original_height - target_height) / 2
            cropped_clip = video_clip.crop(x1=0, y1=crop_y_start, width=original_width, height=target_height)

        return cropped_clip
