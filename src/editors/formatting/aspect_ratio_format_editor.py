from pydantic import validator
from ..base_editor import BaseEditor

class AspectRatioFormatter(BaseEditor):
    aspect_ratio: str

    # @validator('aspect_ratio')
    # def validate_aspect_ratio(cls, v):
    #     try:
    #         width, height = map(float, v.split(':'))
    #         if width <= 0 or height <= 0:
    #             raise ValueError("Width and height must be positive numbers.")
    #         return v
    #     except ValueError:
    #         raise ValueError("Aspect ratio must be in 'width:height' format and contain valid numbers.")

    # def parsed_aspect_ratio(self):
    #     width, height = map(float, self.aspect_ratio.split(':'))
    #     return width / height
    
    def _parse_aspect_ratio(self, aspect_ratio):
        """
        Parses the aspect ratio string and returns a numerical ratio.
        Aspect ratio should be in the format 'width:height' (e.g., '9:16').
        """
        width, height = aspect_ratio.split(':')
        return float(width) / float(height)

    def apply(self, video_clip):
        """
        Reformats a video clip to the specified aspect ratio.

        :return: moviepy.editor.VideoFileClip, the reformatted video clip
        """
        aspect_ratio = self._parse_aspect_ratio(self.aspect_ratio)
        original_width, original_height = video_clip.size

        # Calculate the target dimensions based on the desired aspect ratio
        target_width = original_height * aspect_ratio

        if target_width <= original_width:
            crop_x_start = (original_width - target_width) / 2
            cropped_clip = video_clip.crop(x1=crop_x_start, y1=0, width=target_width, height=original_height)
        else:
            target_height = original_width / aspect_ratio
            crop_y_start = (original_height - target_height) / 2
            cropped_clip = video_clip.crop(x1=0, y1=crop_y_start, width=original_width, height=target_height)

        return cropped_clip
