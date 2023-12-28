from moviepy.editor import VideoFileClip
import time, os

from pipeline.video_pipeline import VideoEditingPipeline
from pipeline.tasks.clipping_task import ClippingTask
from pipeline.tasks.caption_adder_task import CaptionAdderTask
from pipeline.tasks.formatting_task import FormattingTask
from editors.clipping.random_clip_editor import RandomClipEditor
from editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from editors.captioning.caption_adder import CaptionAdder

# Create pipeline
pipeline = VideoEditingPipeline()

# Add tasks
pipeline.add_task(ClippingTask(RandomClipEditor(0, 30)))
pipeline.add_task(FormattingTask(AspectRatioFormatter('9:16')))
pipeline.add_task(CaptionAdderTask(CaptionAdder()))

directory = "../example_videos/example_samples"
for filename in os.listdir(directory):
    if filename.endswith(".mp4"):

        unique_id = int(time.time())
        # Load the original video clip
        original_video = VideoFileClip(os.path.join(directory, filename))
        # Execute pipeline on video
        filename = filename.split(".mp4")[0]
        final_clipped_video = pipeline.execute(original_video)
        output_filename = f"../output/{filename}_clip_{unique_id}.mp4"
        final_clipped_video.write_videofile(output_filename, codec="libx264", fps=24)


