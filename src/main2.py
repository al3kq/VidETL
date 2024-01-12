from pipeline.video_pipeline import VideoEditingPipeline
from editors.clipping.random_clip_editor import RandomClipEditor
from editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from editors.captioning.caption_adder import CaptionAdder

from pipeline.pipeline_execute import execute_pipeline_from_dir
from io_files.video_writer import save_video_files


# Create pipeline
pipeline = VideoEditingPipeline()

# Add tasks
pipeline.add_task(RandomClipEditor(0, 15))
pipeline.add_task(AspectRatioFormatter('4:9'))
pipeline.add_task(CaptionAdder())

directory = "../example_videos/example_samples"
clip = execute_pipeline_from_dir(directory, pipeline)

# Save files util function (to move to io)
save_video_files(clip, "../output")
