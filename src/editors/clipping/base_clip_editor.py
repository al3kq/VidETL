from moviepy.editor import VideoFileClip

class BaseClipEditor:
    def __init__(self):
        # Initialization can include shared properties or configurations
        # common to all clip editing tasks, if any.
        pass

    def apply(self, video_clip):
        """
        This method should be implemented by subclasses to apply specific editing
        operations to the provided video clip.

        :param video_clip: moviepy.editor.VideoFileClip, the video clip to be edited
        :return: moviepy.editor.VideoFileClip, the edited video clip
        """
        raise NotImplementedError("Subclasses should implement this method.")
