from moviepy.editor import VideoFileClip

from pipeline.video_pipeline import VideoEditingPipeline
from pipeline.tasks.clipping_task import ClippingTask
from pipeline.tasks.caption_generator_task import CaptionGeneratorTask
from pipeline.tasks.caption_adder_task import CaptionAdderTask
from pipeline.tasks.formatting_task import FormattingTask
from editors.clipping.random_clip_editor import RandomClipEditor
from editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from editors.captioning.caption_adder import CaptionAdder

from utils.audio_utils import extract_audio, generate_captions


video_file_path = "../example_videos/example_samples/roger_clip.mp4"

# Load the original video clip
original_video = VideoFileClip(video_file_path)

# Create pipeline
pipeline = VideoEditingPipeline()

# Add tasks
pipeline.add_task(ClippingTask(RandomClipEditor(0, 30)))
pipeline.add_task(FormattingTask(AspectRatioFormatter('9:16')))
pipeline.add_task(CaptionAdderTask(CaptionAdder()))

# Execute pipeline on video
final_clipped_video = pipeline.execute(original_video)

output_filename = "output_vid1.mp4"
final_clipped_video.write_videofile(output_filename, codec="libx264", fps=24)


