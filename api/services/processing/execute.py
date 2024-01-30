from src.pipeline.pipeline_execute import execute_pipeline_from_dir
from src.utils.video_utils import match_and_combine_clips
from src.io_files.video_writer import save_video_files

def execute_pipeline(input_dir, output_dir, pipeline):
    try:
        clips = execute_pipeline_from_dir(input_dir, pipeline)
        save_video_files(clips, output_dir)
        print("DONE DONE DONE")
    except Exception as e:
        raise RuntimeError(f"An error occurred during pipeline execution: {e}")
