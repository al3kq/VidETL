class VideoEditingPipeline:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def execute(self, video_clip):
        for task in self.tasks:
            result = task.apply(video_clip)
            video_clip = result

        return video_clip