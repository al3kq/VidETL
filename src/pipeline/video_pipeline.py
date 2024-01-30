from pydantic import BaseModel
from typing import List
from ..editors.base_editor import BaseEditor
import time

class VideoEditingPipeline(BaseModel):
    tasks: List[BaseEditor] = []
    name: str
    status: str = 'created'

    def add_task(self, task):
        self.tasks.append(task)

    def execute(self, video_clip):
        self.status = "proccesing"
        for task in self.tasks:
            print(task)
            start_time =  time.time()
            result = task.apply(video_clip)
            video_clip = result
            print(f"Task time: {time.time() - start_time}")

        self.status = "writing"
        return video_clip