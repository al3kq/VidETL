class CaptionAdderTask:
    def __init__(self, caption_adder, json_captions):
        self.caption_adder = caption_adder
        self.json_captions = json_captions

    def apply(self, video_clip):
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        return self.caption_adder.add_captions(video_clip, self.json_captions)
