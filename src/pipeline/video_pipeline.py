from pydantic import BaseModel
from typing import List
from ..editors.base_editor import BaseEditor

class VideoEditingPipeline(BaseModel):
    tasks: List[BaseEditor] = []
    name: str
    status: str = 'created'

    def add_task(self, task):
        self.tasks.append(task)

    def execute(self, video_clip):
        self.status = "proccesing"
        for task in self.tasks:
            result = task.apply(video_clip)
            video_clip = result

        self.status = "writing"
        return video_clip