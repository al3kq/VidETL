from .base_format_editor import BaseFormatEditor

class AspectRatioFormatter(BaseFormatEditor):
    def __init__(self, aspect_ratio):
        self.aspect_ratio = self._parse_aspect_ratio(aspect_ratio)

    def _parse_aspect_ratio(self, aspect_ratio):
        """
        Parses the aspect ratio string and returns a numerical ratio.
        Aspect ratio should be in the format 'width:height' (e.g., '9:16').
        """
        width, height = aspect_ratio.split(':')
        return float(width) / float(height)
    
    # def apply(self, video_clip):
    #     original_width, original_height = video_clip.size
    #     target_aspect_ratio = self.aspect_ratio

    #     # Calculate the scale factors
    #     scale_w = target_aspect_ratio * original_height / original_width
    #     scale_h = original_width / (target_aspect_ratio * original_height)

    #     # Determine the new dimensions
    #     if scale_w >= 1:
    #         # Need to add letterbox to the sides
    #         new_height = original_height
    #         new_width = int(original_height * target_aspect_ratio)
    #     else:
    #         # Need to add letterbox to the top and bottom
    #         new_width = original_width
    #         new_height = int(original_width / target_aspect_ratio)

    #     # Resize the clip and add black bars to maintain aspect ratio
    #     resized_clip = video_clip.resize(newsize=(new_width, new_height))
    #     final_clip = resized_clip.margin(
    #         left=(new_width - original_width) // 2 if scale_w >= 1 else 0,
    #         top=(new_height - original_height) // 2 if scale_w < 1 else 0,
    #         color=(0, 0, 0)
    #     )

    #     return final_clip



    def apply(self, video_clip):
        """
        Reformats a video clip to the specified aspect ratio.

        :return: moviepy.editor.VideoFileClip, the reformatted video clip
        """
        original_width, original_height = video_clip.size

        # Calculate the target dimensions based on the desired aspect ratio
        target_width = original_height * self.aspect_ratio

        if target_width <= original_width:
            crop_x_start = (original_width - target_width) / 2
            cropped_clip = video_clip.crop(x1=crop_x_start, y1=0, width=target_width, height=original_height)
        else:
            target_height = original_width / self.aspect_ratio
            crop_y_start = (original_height - target_height) / 2
            cropped_clip = video_clip.crop(x1=0, y1=crop_y_start, width=original_width, height=target_height)

        return cropped_clip
