from pipeline.video_pipeline import VideoEditingPipeline
from editors.captioning.caption_adder import CaptionAdder
from editors.summary.summarize import Summarizer

from pipeline.pipeline_execute import execute_pipeline_from_dir
from io_files.video_writer import save_video_files


pipeline = VideoEditingPipeline()
pipeline.add_task(Summarizer())

directory = "../example_videos/smart_vid"
clip = execute_pipeline_from_dir(directory, pipeline)

# Save files util function (to move to io)
# save_video_files(clip, "../output")