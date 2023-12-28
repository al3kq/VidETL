class ClippingTask:
    def __init__(self, editor):
        self.editor = editor

    def apply(self, video_clip):
        return self.editor.edit(video_clip)
