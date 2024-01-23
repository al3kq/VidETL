import json
from src.pipeline.video_pipeline import VideoEditingPipeline
from src.editors.clipping.random_clip_editor import RandomClipEditor
from src.editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from src.editors.captioning.caption_adder import CaptionAdder
from src.pipeline.pipeline_execute import execute_pipeline_from_dir
from src.utils.video_utils import match_and_combine_clips
from src.io_files.video_writer import save_video_files

# Function to create an editor instance based on the type and parameters
def create_editor(editor_data):
    editor_type = editor_data['type']
    config_data = editor_data.get('config', None)
    if editor_type == 'RandomClipEditor':
        return RandomClipEditor(start_time=int(config_data.get('start', 0)), duration=int(config_data.get('end', 30)), silent=config_data.get('silent', False))
    elif editor_type == 'AspectRatioFormatter':
        return AspectRatioFormatter(aspect_ratio=config_data['aspect_ratio'])
    elif editor_type == 'CaptionAdder':
        return CaptionAdder(editable=config_data.get('editable', False), highlight_words=config_data.get('highlight_words', False))
    else:
        raise ValueError(f"Unknown editor type: {editor_type}")

# In services/json_to_pipe.py

def json_to_pipeline(pipeline_config: dict):
    pipeline_name = pipeline_config["name"]
    tasks_config = pipeline_config["tasks"]
    input_directory = pipeline_config["directory"]
    output_directory = pipeline_config.get("output_directory", "./output")

    # Create a list of editor instances based on the task configurations
    pipeline_tasks = [create_editor(task) for task in tasks_config]

    # Initialize the pipeline with the created tasks
    pipeline = VideoEditingPipeline(name=pipeline_name, tasks=pipeline_tasks)

    # Execute the pipeline and save the output
    clip = execute_pipeline_from_dir(input_directory, pipeline)
    save_video_files(clip, output_directory)

    return pipeline

