from moviepy.editor import CompositeVideoClip, ImageClip
import time
from .utils.write_captions import get_caption_json, get_editable_caption_json
from .utils.gen_captions import generate_highlighted_caption_image,generate_caption_image
from ..base_editor import BaseEditor
from ...utils.file_utils import gen_temp_file_name

class CaptionAdder(BaseEditor):
    caption_font: str = 'Verdana'
    caption_fontsize: int = 50
    caption_color: str = 'white'
    highlight_words: bool = False
    editable: bool = False

    def _gen_image_clip(self, temp_file, video_width, video_height, start_time, end_time):
        image_clip = ImageClip(temp_file)
        image_x_position = (video_width - image_clip.size[0])/2
        offset_from_bottom = 25
        image_y_position = video_height - image_clip.size[1] - offset_from_bottom
        return image_clip.set_pos((image_x_position, image_y_position)).set_start(start_time).set_duration(end_time - start_time)

    def apply(self, video_clip):
        clips = [video_clip]  # Start with the original clip
        if self.editable:
            caption_json = get_editable_caption_json(video_clip)
        else:
            caption_json = get_caption_json(video_clip)

        # caption_json = self.get_caption_json(video_clip)
        video_width, video_height = video_clip.size

        # Reference dimensions (e.g., 640x720)
        ref_width, ref_height = 640, 720

        # Calculate the scaling factor based on width (or height)
        scale_factor = video_width / ref_width

        # Adjust font size based on the scaling factor
        adjusted_fontsize = int(self.caption_fontsize * scale_factor)

        print("adding captions")

        for segment in caption_json['segments']:
            words_in_segment = segment['words']
            # Split the segment into chunks of 3 words
            for i in range(0, len(words_in_segment), 3):
                chunk = words_in_segment[i:i+3]
                chunk_start = chunk[0]["start"]
                chunk_end = chunk[-1]["end"]
                
                # Constructing caption from words in the chunk
                caption = ' '.join(word['text'] for word in chunk)

                if self.highlight_words:
                    for word_index, word_info in enumerate(chunk):
                        word_start, word_end = word_info['start'], word_info['end']

                        temp_file = gen_temp_file_name("temp", "png")

                        generate_highlighted_caption_image(caption, word_info["text"], word_index, temp_file, font_size=adjusted_fontsize)
                        image_clip = self._gen_image_clip(temp_file, video_width, video_height, word_start, word_end)

                        # Add the text clip to the list of clips
                        clips.append(image_clip)
                else:
                    temp_file = gen_temp_file_name("temp", "png")
                    generate_caption_image(caption, temp_file, font_size=adjusted_fontsize)
                    image_clip = self._gen_image_clip(temp_file, video_height, video_width, chunk_start, chunk_end)

                    # Add the text clip to the list of clips
                    clips.append(image_clip)

        # Composite all clips (original and text clips) together
        video_with_captions = CompositeVideoClip(clips)
        # subprocess.call(['sh', 'cltemp.sh'])

        return video_with_captions
