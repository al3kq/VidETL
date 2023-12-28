from moviepy.editor import TextClip, CompositeVideoClip

class CaptionAdder:
    def __init__(self, video_clip, json_captions, caption_font='Arial', caption_fontsize=24, caption_color='white'):
        self.video_clip = video_clip
        self.json_captions = json_captions
        self.caption_font = caption_font
        self.caption_fontsize = caption_fontsize
        self.caption_color = caption_color

    def add_captions(self):
        clips = [self.video_clip]  # Start with the original clip

        for segment in self.json_captions['segments']:
            for word_info in segment['words']:
                word = word_info['text']
                start_time = word_info['start']
                end_time = word_info['end']

                # Create a TextClip for each word
                txt_clip = TextClip(word, fontsize=self.caption_fontsize, font=self.caption_font, color=self.caption_color)
                txt_clip = txt_clip.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

                outline_txt = TextClip(word, fontsize=self.caption_fontsize+2, font=self.caption_font, color="black")
                outline_txt_clip = outline_txt.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

                # Add the text clip to the list of clips
                clips.append(outline_txt_clip)
                clips.append(txt_clip)

        # Composite all clips (original and text clips) together
        video_with_captions = CompositeVideoClip(clips)

        return video_with_captions
