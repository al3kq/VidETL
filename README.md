### Video Editing automation workflow pipeline.

Editing tasks added:

* Generate and add timestamped captions
* Select timestamped/random clip
* Change aspect ratio

Current structure:

VideoEditingPipeline:
    - add editing tasks to the pipeline
        - each (editing) task expects a VideoClip as an input and output
    - execute() loops through added tasks feeding output to next editing task
