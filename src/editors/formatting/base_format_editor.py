class BaseFormatEditor:
    def __init__(self, video_clip):
        self.video_clip = video_clip

    def apply_format(self):
        raise NotImplementedError("This method should be implemented by subclasses.")
