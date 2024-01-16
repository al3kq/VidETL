
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('jsonForm');
    const addTaskBtn = document.getElementById('addTaskBtn');
    const tasksContainer = document.getElementById('tasks');
    const outputJSON = document.getElementById('outputJSON');

    function createTaskInputs(taskType) {
        switch (taskType) {
            case 'RandomClipEditor':
                return `
                    <label>Start Time:</label>
                    <input type="number" name="start_time" min="0" step="0.1">
                    <label>Duration:</label>
                    <input type="number" name="duration" min="0" step="0.1">
                `;
            case 'AspectRatioFormatter':
                return `
                    <label>Aspect Ratio:</label>
                    <input type="text" name="aspect_ratio">
                `;
            case 'CaptionAdder':
                return `
                    <label>Editable:</label>
                    <input type="checkbox" name="editable">
                    <label>Highlight Words:</label>
                    <input type="checkbox" name="highlight_words">
                `;
            default:
                return '';
        }
    }

    addTaskBtn.addEventListener('click', function () {
        const taskDiv = document.createElement('div');
        taskDiv.classList.add('task');
        taskDiv.innerHTML = `
            <label>Task Type:</label>
            <select name="taskType" class="taskType">
                <option value="">Select Task</option>
                <option value="RandomClipEditor">RandomClipEditor</option>
                <option value="AspectRatioFormatter">AspectRatioFormatter</option>
                <option value="CaptionAdder">CaptionAdder</option>
            </select>
            <div class="taskConfig"></div>
            <button type="button" class="removeTaskBtn">Remove Task</button>
        `;
        tasksContainer.appendChild(taskDiv);
    });

    tasksContainer.addEventListener('change', function (e) {
        if (e.target.classList.contains('taskType')) {
            const taskType = e.target.value;
            const taskConfigDiv = e.target.nextElementSibling;
            taskConfigDiv.innerHTML = createTaskInputs(taskType);
        }
    });

    tasksContainer.addEventListener('click', function (e) {
        if (e.target.className === 'removeTaskBtn') {
            e.target.parentElement.remove();
        }
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(form);
        const json = {
            pipeline: {
                name: formData.get('pipelineName'),
                tasks: [],
                directory: formData.get('directory')
            },
            output_directory: "output"
        };
        document.querySelectorAll('.task').forEach(taskDiv => {
            const taskType = taskDiv.querySelector('.taskType').value;
            const taskConfig = {};
            taskDiv.querySelectorAll('.taskConfig input').forEach(input => {
                if (input.type === 'checkbox') {
                    taskConfig[input.name] = input.checked;
                } else {
                    taskConfig[input.name] = input.value ? input.value : undefined;
                }
            });
            if (taskType) {
                json.pipeline.tasks.push({ type: taskType, ...taskConfig });
            }
        });
        console.log(json)
        // Fetch API to POST the data to localhost:8000/pipeline
        fetch('http://localhost:8000/pipeline', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(json)
        })
            .then(response => response.json())
            .then(data => {
                outputJSON.textContent = 'Response: ' + JSON.stringify(data, null, 2);
            })
            .catch(error => {
                outputJSON.textContent = 'Error: ' + error;
            });
    });
});
