class CaptionGeneratorTask:
    def __init__(self, caption_generator):
        self.caption_generator = caption_generator

    def apply(self, video_clip):
        # Assuming the generate_captions method returns a JSON of captions
        json_captions = self.caption_generator.generate_captions(video_clip)
        return json_captions
