import json
from src.pipeline.video_pipeline import VideoEditingPipeline
from src.editors.clipping.random_clip_editor import RandomClipEditor
from src.editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from src.editors.captioning.caption_adder import CaptionAdder

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
    pipeline_config = pipeline_data["pipeline"]
    try: 
        pipeline_name = pipeline_config["name"]
        tasks_config = pipeline_config["tasks"]
        pipeline_tasks = [create_editor(task) for task in tasks_config]
        # Initialize the pipeline with the created tasks
        pipeline = VideoEditingPipeline(name=pipeline_name, tasks=pipeline_tasks)
        return pipeline

    except KeyError as e:
        raise ValueError(f"Invalid pipeline configuration: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred during pipeline execution: {e}")


