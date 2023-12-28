from utils.audio_utils import extract_audio, generate_captions
import time, os

class CaptionAdderTask:
    def __init__(self, caption_adder):
        self.caption_adder = caption_adder

    def apply(self, video_clip):
        unique_id = int(time.time()) 
        audio_filename = f"output_{unique_id}.wav"
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        extract_audio(video_clip, audio_filename)
        caption_json = generate_captions(audio_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        return self.caption_adder.add_captions(video_clip, caption_json)
