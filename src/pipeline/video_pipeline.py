class VideoEditingPipeline:
    def __init__(self):
        self.tasks = []
        self.additional_data = {}

    def add_task(self, task, output_key=None):
        self.tasks.append((task, output_key))

    def execute(self, video_clip):
        for task, output_key in self.tasks:
            result = task.apply(video_clip, self.additional_data)

            if output_key:
                self.additional_data[output_key] = result
            else:
                video_clip = result

        return video_clip
