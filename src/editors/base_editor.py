from pydantic import BaseModel

class BaseEditor(BaseModel):

    def apply(self, video_clip):
        raise NotImplementedError("This method should be implemented in subclasses")
