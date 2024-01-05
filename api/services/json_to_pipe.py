import json
from src.pipeline.video_pipeline import VideoEditingPipeline
from src.editors.clipping.random_clip_editor import RandomClipEditor
from src.editors.formatting.aspect_ratio_format_editor import AspectRatioFormatter
from src.editors.captioning.caption_adder import CaptionAdder
from src.pipeline.pipeline_execute import execute_pipeline_from_dir
from src.utils.video_utils import match_and_combine_clips
from src.io_files.video_writer import save_video_files

top_bottom_clips = []

# Path to your JSON file
json_file_path = 'main_ex.json'

pipeline_data = None
# Open the file and load JSON content
with open(json_file_path, 'r') as file:
    pipelines_data = json.load(file)
# Function to create an editor instance based on the type and parameters
def create_editor(editor_data):
    editor_type = editor_data['type']
    if editor_type == 'RandomClipEditor':
        return RandomClipEditor(start_time=editor_data.get('start', 0), duration=editor_data.get('end', 30), silent=editor_data.get('silent', False))
    elif editor_type == 'AspectRatioFormatter':
        return AspectRatioFormatter(aspect_ratio=editor_data['aspectRatio'])
    elif editor_type == 'CaptionAdder':
        return CaptionAdder()
    else:
        raise ValueError(f"Unknown editor type: {editor_type}")

# Process each pipeline
for pipeline_data in pipelines_data['pipelines']:
    pipeline = VideoEditingPipeline()
    for task_data in pipeline_data['tasks']:
        editor = create_editor(task_data)
        pipeline.add_task(editor)
    
    # Execute the pipeline
    top_bottom_clips.append(execute_pipeline_from_dir(pipeline_data['directory'], pipeline))

# Handle post-processing
post_processing = pipelines_data.get('postProcessing', {})
if 'matchAndCombineClips' in post_processing:
    # Assuming you have a way to retrieve the output of pipelines
    top_clips = top_bottom_clips[0]  # Retrieve top clips
    bottom_clips = top_bottom_clips[1]  # Retrieve bottom clips
    combined_clips = match_and_combine_clips(top_clips, bottom_clips)
    save_video_files(combined_clips, post_processing['saveDirectory'])
