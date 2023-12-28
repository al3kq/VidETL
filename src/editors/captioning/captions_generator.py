import whisper_timestamped as whisper

class CaptionGenerator:
    def __init__(self, audio_file_path):
        self.audio_file_path = audio_file_path

    def generate_captions(self): 
        audio = whisper.load_audio(self.audio_file_path)
        model = whisper.load_model("tiny", device="cpu")
        result = whisper.transcribe(model, audio, language="en")
        return result
