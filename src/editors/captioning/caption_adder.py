from moviepy.editor import TextClip, CompositeVideoClip
import time, os
from utils.audio_utils import extract_audio, generate_captions

class CaptionAdder:
    def __init__(self, caption_font='Arial', caption_fontsize=48, caption_color='white'):
        self.caption_font = caption_font
        self.caption_fontsize = caption_fontsize
        self.caption_color = caption_color

    def get_caption_json(self, video_clip):
        unique_id = int(time.time()) 
        audio_filename = f"output_{unique_id}.wav"
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        extract_audio(video_clip, audio_filename)
        caption_json = generate_captions(audio_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        return caption_json

    def apply(self, video_clip):
        clips = [video_clip]  # Start with the original clip
        caption_json = self.get_caption_json(video_clip)

        for segment in caption_json['segments']:
            for word_info in segment['words']:
                if word_info["confidence"] > 0.2:
                    word = word_info['text']
                    start_time = word_info['start']
                    end_time = word_info['end']

                    # Create a TextClip for each word
                    txt_clip = TextClip(word, fontsize=self.caption_fontsize, font=self.caption_font, color=self.caption_color, stroke_color='black', stroke_width=2)
                    txt_clip = txt_clip.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

                    # outline_txt = TextClip(word, fontsize=self.caption_fontsize+2, font=self.caption_font, color="black")
                    # outline_txt_clip = outline_txt.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

                    # Add the text clip to the list of clips
                    # clips.append(outline_txt_clip)
                    clips.append(txt_clip)

        # Composite all clips (original and text clips) together
        video_with_captions = CompositeVideoClip(clips)

        return video_with_captions
