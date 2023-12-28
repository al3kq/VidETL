from utils.audio_utils import extract_audio, generate_captions
import time, os

class CaptionAdderTask:
    def __init__(self, caption_adder):
        self.caption_adder = caption_adder

    def apply(self, video_clip):
        return self.caption_adder.add_captions(video_clip)
