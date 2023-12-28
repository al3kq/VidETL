class FormattingTask:
    def __init__(self, editor):
        self.editor = editor

    def apply(self, video_clip):
        return self.editor.apply_format(video_clip)
