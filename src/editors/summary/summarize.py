from moviepy.editor import VideoFileClip
from openai import OpenAI
from utils.audio_utils import extract_audio, generate_captions
import time, os
from dotenv import load_dotenv
from fuzzywuzzy import fuzz 

class Summarizer:
    def __init__(self):
        # Initialization can include shared properties or configurations
        # common to all clip editing tasks, if any.
        pass

    def apply(self, video_clip):
        api_key=os.environ.get("OPENAI_API_KEY")
        audio = video_clip.audio
        print(api_key)
        self.client = OpenAI(api_key=api_key)
        captions = self.get_caption_json(video_clip)

        # Example usage
        text_summary = self.summarize_text(captions['text'])
        prompt = f"Find segments related to '{text_summary}'"
        prompt = prompt + "\n" + self.get_segments(captions)

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant and designed to output JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        key_phrase = response.choices[0].message.content
        print(key_phrase)
        print("======================================================")
        segments = self.find_matching_segments(key_phrase, captions)
        for seg in segments:
            print(seg[0], end=" ")
        video_clip = video_clip.set_audio(audio)
        return video_clip


    def get_caption_json(self, video_clip):
        unique_id = int(time.time()) 
        audio_filename = f"output_{unique_id}.wav"
        # Assuming the add_captions method applies captions to the clip and returns the modified clip
        extract_audio(video_clip, audio_filename)
        caption_json = generate_captions(audio_filename)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        return caption_json
    
    def get_segments(self, captions):
        segment_string = ""
        for segment in captions['segments']:
            segment_text = segment['text'].lower()
            segment_string += segment_text + "\n"
        return segment_string
    
    def summarize_text(self, text):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                {"role": "user", "content": f"Summarize the following text into main ideas:\n\n{text}"}
            ]
        )
        return response.choices[0].message.content

    def find_matching_segments(self, key_phrase, json_data):
        matching_segments = []
        for segment in json_data['segments']:
            segment_text = segment['text'].lower()
            if fuzz.partial_ratio(key_phrase.lower(), segment_text) > 70:  # Adjust the threshold as needed
                for word in segment['words']:
                    matching_segments.append((word['text'], word['start'], word['end']))
        return matching_segments



