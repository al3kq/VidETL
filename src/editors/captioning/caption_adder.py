from moviepy.editor import CompositeVideoClip, ImageClip
import time, os
from utils.audio_utils import extract_audio, generate_captions, generate_captions_file
from utils.caption_utils import generate_highlighted_caption_image, get_low_confidence_words, generate_caption_image
from ..base_editor import BaseEditor
import json

class CaptionAdder(BaseEditor):
    caption_font: str = 'Verdana'
    caption_fontsize: int = 50
    caption_color: str = 'white'
    highlight_words: bool = False
    editable: bool = False

    def get_caption_json(self, video_clip):
        unique_id = int(time.time()) 
        audio_filename = f"output_{unique_id}.wav"
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        extract_audio(video_clip, audio_filename)
        caption_json = generate_captions(audio_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        return caption_json
    
    def get_caption_file(self, video_clip, output_file):
        unique_id = int(time.time()) 
        audio_filename = f"output_{unique_id}.wav"
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        extract_audio(video_clip, audio_filename)
        generate_captions_file(audio_filename, output_file)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
    
    def get_editable_caption_json(self, video_clip):
        unique_id = int(time.time()) 
        caption_output_file = f"output_captions_{unique_id}.json"
        self.get_caption_file(video_clip, caption_output_file)


        # Open and print low confidence words
        try:
            with open(caption_output_file, 'r') as file:
                caption_json = json.load(file)
                low_confidence = get_low_confidence_words(caption_json, 0.8)
                if len(low_confidence) > 0:
                    print(low_confidence)

        except FileNotFoundError:
            print(f"File not found: {caption_output_file}")

        # Prompt User:
        while True:
            user_input = input("Are the captions ready? (y/Y/yes to proceed): ")
            if user_input.lower() == 'y' or user_input.lower() == 'yes':
                break

        try:
            with open(caption_output_file, 'r') as file:
                caption_json = json.load(file)
                return caption_json
        except FileNotFoundError:
            print(f"File not found: {caption_output_file}")


    def apply(self, video_clip):
        clips = [video_clip]  # Start with the original clip
        if self.editable:
            caption_json = self.get_editable_caption_json(video_clip)
        else:
            caption_json = self.get_caption_json(video_clip)

        # caption_json = self.get_caption_json(video_clip)
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
                chunk_start = chunk[0]["start"]
                chunk_end = chunk[-1]["end"]
                
                # Constructing caption from words in the chunk
                caption = ' '.join(word['text'] for word in chunk)

                if self.highlight_words:
                    for word_index, word_info in enumerate(chunk):
                        word_start, word_end = word_info['start'], word_info['end']

                        temp_dir = "temp"
                        unique_id = int(time.time())
                        temp_file = f"{temp_dir}/test_{unique_id}.png"

                        generate_highlighted_caption_image(caption, word_info["text"], word_index, temp_file, font_size=adjusted_fontsize)


                        image_clip = ImageClip(temp_file)
                        image_x_position = (video_width - image_clip.size[0])/2
                        offset_from_bottom = 25
                        image_y_position = video_height - image_clip.size[1] - offset_from_bottom



                        cat = image_clip.set_pos((image_x_position, image_y_position)).set_start(word_start).set_duration(word_end - word_start)

                    # Add the text clip to the list of clips
                        clips.append(cat)
                else:
                    temp_dir = "temp"
                    unique_id = int(time.time())
                    temp_file = f"{temp_dir}/test_{unique_id}.png"
                    generate_caption_image(caption, temp_file, font_size=adjusted_fontsize)
                    image_clip = ImageClip(temp_file)
                    image_x_position = (video_width - image_clip.size[0])/2
                    offset_from_bottom = 25
                    image_y_position = video_height - image_clip.size[1] - offset_from_bottom

                    cat = image_clip.set_pos((image_x_position, image_y_position)).set_start(chunk_start).set_duration(chunk_end - chunk_start)

                    # Add the text clip to the list of clips
                    clips.append(cat)

        # Composite all clips (original and text clips) together
        video_with_captions = CompositeVideoClip(clips)
        # subprocess.call(['sh', 'cltemp.sh'])

        return video_with_captions
