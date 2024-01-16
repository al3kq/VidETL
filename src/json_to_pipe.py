import json
from pipeline.video_pipeline import VideoEditingPipeline
from editors.clipping.random_clip_editor import RandomClipEditor
from editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from editors.captioning.caption_adder import CaptionAdder
from pipeline.pipeline_execute import execute_pipeline_from_dir
from io_files.video_writer import save_video_files

# Function to create an editor instance based on the type and parameters
def create_editor(editor_data):
    editor_type = editor_data['type']
    if editor_type == 'RandomClipEditor':
        return RandomClipEditor(
            start_time=editor_data.get('start', 0),
            duration=editor_data.get('end', 30),
            silent=editor_data.get('silent', False)
        )
    elif editor_type == 'AspectRatioFormatter':
        return AspectRatioFormatter(aspect_ratio=editor_data['aspect_ratio'])
    elif editor_type == 'CaptionAdder':
        return CaptionAdder(
            highlight_words=editor_data.get('highlight_words', False),
            editable=editor_data.get('editable', False)
        )
    else:
        raise ValueError(f"Unknown editor type: {editor_type}")

# Load JSON data from file
json_file_path = 'example_json/main2_json.json'
with open(json_file_path, 'r') as file:
    all_data = json.load(file)

# Process and setup the pipeline
pipeline_data = all_data["pipeline"]
pipeline_tasks = [create_editor(task) for task in pipeline_data["tasks"]]
pipeline = VideoEditingPipeline(name=pipeline_data["name"], tasks=pipeline_tasks)

# Execute the pipeline and save the output
input_directory = pipeline_data["directory"]
output_directory = all_data["output_directory"]
clip = execute_pipeline_from_dir(input_directory, pipeline)
save_video_files(clip, output_directory)