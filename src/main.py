from pipeline.video_pipeline import VideoEditingPipeline
from editors.clipping.random_clip_editor import RandomClipEditor
from editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from editors.captioning.caption_adder import CaptionAdder

from pipeline.pipeline_execute import execute_pipeline_from_dir
from utils.video_utils import match_and_combine_clips
from io_files.video_writer import save_video_files


# Create pipeline
pipeline = VideoEditingPipeline(name="top")

# Add tasks
pipeline.add_task(RandomClipEditor(start_time=0, duration=10))
pipeline.add_task(AspectRatioFormatter(aspect_ratio='8:9'))
pipeline.add_task(CaptionAdder(editable=True, highlight_words=True))

directory = "../example_videos/example_samples"
top_clips = execute_pipeline_from_dir(directory, pipeline)

# Seperate pipeline for bottom clips
bottom_pipeline = VideoEditingPipeline(name="bottom")
bottom_pipeline.add_task(RandomClipEditor(start_time=0, duration=10, silent=True))
bottom_pipeline.add_task(AspectRatioFormatter(aspect_ratio='8:9'))

bottom_dir = "../example_videos/bottom"
bottom_clips = execute_pipeline_from_dir(bottom_dir, bottom_pipeline)

# Combine clips top/bottom util function
combined_clips = match_and_combine_clips(top_clips, bottom_clips)

# Save files util function (to move to io)
save_video_files(combined_clips, "../output")
