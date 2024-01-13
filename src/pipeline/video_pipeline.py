from pydantic import BaseModel
from typing import List
from editors.base_editor import BaseEditor

class VideoEditingPipeline(BaseModel):
    tasks: List[BaseEditor] = []
    name: str

    def add_task(self, task):
        self.tasks.append(task)

    def execute(self, video_clip):
        for task in self.tasks:
            result = task.apply(video_clip)
            video_clip = result

        return video_clip