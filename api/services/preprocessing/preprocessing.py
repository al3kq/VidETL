from fastapi import HTTPException
from src.pipeline.video_pipeline import VideoEditingPipeline
from src.editors.clipping.random_clip_editor import RandomClipEditor
from src.editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from src.editors.captioning.caption_adder import CaptionAdder
from src.pipeline.pipeline_execute import execute_pipeline_from_dir
from src.utils.video_utils import match_and_combine_clips
from src.io_files.video_writer import save_video_files

def parse_pipeline_data(pipeline_data, user_id, file_paths):
    try:
        pipeline_body = pipeline_data["body"]
        pipeline_config = pipeline_body["pipeline"]
        output_directory = pipeline_body.get("output_directory", "./output")
        if pipeline_config["directory"] == '' and file_paths[user_id] != "":
            pipeline_config["directory"] = file_paths.get(user_id, "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Error parsing JSON"))
    return pipeline_config, output_directory

# Function to create an editor instance based on the type and parameters
def create_editor(editor_data):
    try:
        editor_type = editor_data['type']
        config_data = editor_data.get('config', None)
        if editor_type == 'RandomClipEditor':
            return RandomClipEditor(start_time=int(config_data.get('start_time', 0)), duration=int(config_data.get('duration', 30)), silent=config_data.get('silent', False))
        elif editor_type == 'AspectRatioFormatter':
            return AspectRatioFormatter(aspect_ratio=config_data['aspect_ratio'])
        elif editor_type == 'CaptionAdder':
            return CaptionAdder(editable=config_data.get('editable', False), highlight_words=config_data.get('highlight_words', False))
        else:
            raise ValueError(f"Unknown editor type: {editor_type}")
    except KeyError as e:
        raise ValueError(f"Missing required editor configuration: {e}")

def json_to_pipeline(pipeline_data: dict):
    try: 
        pipeline_config = pipeline_data["pipeline"]
        pipeline_name = pipeline_config["name"]
        tasks_config = pipeline_config["tasks"]
        # Create a list of editor instances based on the task configurations
        pipeline_tasks = [create_editor(task) for task in tasks_config]
        # Initialize the pipeline with the created tasks
        pipeline = VideoEditingPipeline(name=pipeline_name, tasks=pipeline_tasks)

        return pipeline
        # Execute the pipeline and save the output
        clip = execute_pipeline_from_dir(input_directory, pipeline)
        save_video_files(clip, output_directory)

        return pipeline
    except KeyError as e:
        raise ValueError(f"Invalid pipeline configuration: {e}")

