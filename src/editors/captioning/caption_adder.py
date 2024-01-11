from moviepy.editor import TextClip, CompositeVideoClip, ImageClip
import time, os
from utils.audio_utils import extract_audio, generate_captions
from utils.caption_utils import generate_highlighted_caption_image, generate_caption_image
import subprocess

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
        video_width, video_height = video_clip.size

        # Reference dimensions (e.g., 640x720)
        ref_width, ref_height = 640, 720

        # Calculate the scaling factor based on width (or height)
        scale_factor = video_width / ref_width

        # Adjust font size based on the scaling factor
        adjusted_fontsize = int(self.caption_fontsize * scale_factor)

        for segment in caption_json['segments']:
            words_in_segment = segment['words']
            # Split the segment into chunks of 3 words
            for i in range(0, len(words_in_segment), 3):
                chunk = words_in_segment[i:i+3]
                chunk_start_time = chunk[0]['start']
                chunk_end_time = chunk[-1]['end']
                
                # Constructing caption from words in the chunk
                temp_dir = "temp"
                unique_id = int(time.time())
                temp_file = f"{temp_dir}/test_{unique_id}.png"
                caption = ' '.join(word['text'] for word in chunk)

                generate_caption_image(caption, temp_file)

                non_highlighted_caption = ImageClip(temp_file)
                image_x_position = (video_width - non_highlighted_caption.size[0])/2
                offset_from_bottom = 50
                image_y_position = video_height - non_highlighted_caption.size[1] - offset_from_bottom
                # cat = non_highlighted_caption.set_pos((image_x_position, image_y_position)).set_start(chunk_start_time).set_duration(chunk_end_time - chunk_start_time)
                # clips.append(cat)
                for word_info in chunk:
                    word_start, word_end = word_info['start'], word_info['end']

                    temp_dir = "temp"
                    unique_id = int(time.time())
                    temp_file = f"{temp_dir}/test_{unique_id}.png"

                    generate_highlighted_caption_image(caption, word_info["text"], temp_file)


                    image_clip = ImageClip(temp_file)




                    cat = image_clip.set_pos((image_x_position, image_y_position)).set_start(word_start).set_duration(word_end - word_start)

                # Create a TextClip for the chunk with adjusted fontsize
                # txt_clip = TextClip(caption, fontsize=adjusted_fontsize, font=self.caption_font, color=self.caption_color, size=(video_width*1/2, None), bg_color='black', method='caption')
                # txt_clip = txt_clip.set_pos('bottom').set_start(start_time).set_duration(end_time - start_time)

                # Add the text clip to the list of clips
                    clips.append(cat)

        # Composite all clips (original and text clips) together
        video_with_captions = CompositeVideoClip(clips)
        subprocess.call(['sh', 'cltemp.sh'])

        return video_with_captions
