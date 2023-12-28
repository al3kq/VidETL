from utils.audio_utils import extract_audio, generate_captions

class CaptionAdderTask:
    def __init__(self, caption_adder):
        self.caption_adder = caption_adder

    def apply(self, video_clip):
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        extract_audio(video_clip, "output1.wav")
        caption_json = generate_captions("output1.wav")
        return self.caption_adder.add_captions(video_clip, caption_json)
