from utils.audio_utils import extract_audio
import os, time, json
from utils.file_utils import gen_temp_file_name
import whisper_timestamped as whisper

def generate_captions(audio_file_path):
    try:
        start_time = time.time()
        audio = whisper.load_audio(audio_file_path)
        model = whisper.load_model("medium.en", device="cpu")
        result = whisper.transcribe(model, audio, language="en")
        print(f"gen caps time: {time.time() - start_time}")
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def generate_captions_file(audio_file_path, output_file):
    print("her3eee")
    start_time = time.time()
    audio = whisper.load_audio(audio_file_path)
    model = whisper.load_model("medium.en", device="cpu")
    result = whisper.transcribe(model, audio, language="en")
    with open(output_file, 'w') as file:
        json.dump(result, file)
    print(f"gen caps file time: {time.time() - start_time}")

def get_caption_json(video_clip):
    audio_filename = gen_temp_file_name("temp", "wav")
    # Assuming the add_captions method applies captions to the clip and returns the modified clip
    extract_audio(video_clip, audio_filename)
    caption_json = generate_captions(audio_filename)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)
    return caption_json

def get_caption_file(video_clip, output_file):
    audio_filename = gen_temp_file_name("temp", "wav")
    # Assuming the add_captions method applies captions to the clip and returns the modified clip
    extract_audio(video_clip, audio_filename)
    generate_captions_file(audio_filename, output_file)
    if os.path.exists(audio_filename):
        os.remove(audio_filename)


def get_low_confidence_words(caption_data, conf_thres):
    low_conf = ""
    for segments in caption_data["segments"]:
        for word_data in segments["words"]:
            word_data["low_confidence"] = False
            if word_data["confidence"] < conf_thres:
                word = word_data["text"]
                conf = word_data["confidence"]
                low_conf += f"{word}->{conf}"
                word_data["low_confidence"] = True

    return low_conf

def get_editable_caption_json(video_clip):
    caption_output_file = gen_temp_file_name("temp", "json")
    get_caption_file(video_clip, caption_output_file)

    # Open and print low confidence words
    try:
        with open(caption_output_file, 'r') as file:
            caption_json = json.load(file)
            low_confidence = get_low_confidence_words(caption_json, 0.8)
            if len(low_confidence) > 0:
                print(caption_json)
                print("low: ")
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
