document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('jsonForm');
    const tasksContainer = document.getElementById('tasks');
    const outputJSON = document.getElementById('outputJSON');
    const addTaskBtn = document.getElementById('addTaskBtn');

    addTaskBtn.addEventListener('click', function () {
        addTaskSelector();
    });

    tasksContainer.addEventListener('click', function (e) {
        if (e.target.classList.contains('saveTaskBtn')) {
            saveTask(e.target.parentElement);
        } else if (e.target.classList.contains('editTaskBtn')) {
            editTask(e.target.parentElement);
        } else if (e.target.classList.contains('removeTaskBtn')) {
            e.target.parentElement.remove();
        }
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const json = generateJSON();
        outputJSON.textContent = JSON.stringify(json, null, 2);
    });

    function addTaskSelector() {
        const taskSelectorDiv = document.createElement('div');
        taskSelectorDiv.classList.add('task');
        taskSelectorDiv.innerHTML = `
            <label>Task Type:</label>
            <select class="taskTypeSelector">
                <option value="">Select Task Type</option>
                <option value="RandomClipEditor">RandomClipEditor</option>
                <option value="AspectRatioFormatter">AspectRatioFormatter</option>
                <option value="CaptionAdder">CaptionAdder</option>
            </select>
            <div class="taskConfig"></div>
            <button type="button" class="saveTaskBtn">Save Task</button>
        `;
        tasksContainer.appendChild(taskSelectorDiv);
    }

    function saveTask(taskDiv) {
        const taskTypeSelector = taskDiv.querySelector('.taskTypeSelector');
        const taskType = taskTypeSelector.value;
        taskTypeSelector.disabled = true;

        // Display task type
        const taskTypeDisplay = document.createElement('span');
        taskTypeDisplay.textContent = `Task Type: ${taskType}`;
        taskDiv.appendChild(taskTypeDisplay);

        // Iterate through each configuration input to display their values
        const taskConfigDisplay = document.createElement('div');
        taskDiv.querySelectorAll('.taskConfig input').forEach(input => {
            input.disabled = true;

            let configValue = input.type === 'checkbox' ? input.checked : input.value;
            let configText = `${input.name}: ${configValue}`;

            let configDisplay = document.createElement('span');
            configDisplay.textContent = configText;
            taskConfigDisplay.appendChild(configDisplay);
            taskConfigDisplay.appendChild(document.createElement('br')); // Line break for readability
        });

        taskDiv.appendChild(taskConfigDisplay);

        taskDiv.querySelector('.saveTaskBtn').style.display = 'none';

        taskDiv.innerHTML += `
            <button type="button" class="editTaskBtn">Edit</button>
            <button type="button" class="removeTaskBtn">Delete</button>
        `;
    }


    function editTask(taskDiv) {
        taskDiv.querySelector('.taskTypeSelector').disabled = false;
        taskDiv.querySelectorAll('.taskConfig input').forEach(input => {
            input.disabled = false;
        });
        taskDiv.querySelector('.editTaskBtn').style.display = 'none';
        taskDiv.querySelector('.removeTaskBtn').style.display = 'none';
        taskDiv.querySelector('.saveTaskBtn').style.display = 'inline-block';
    }

    tasksContainer.addEventListener('change', function (e) {
        if (e.target.classList.contains('taskTypeSelector')) {
            const taskType = e.target.value;
            const taskConfigDiv = e.target.nextElementSibling;
            taskConfigDiv.innerHTML = createTaskInputs(taskType);
        }
    });

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
            const taskType = taskDiv.querySelector('.taskTypeSelector').value;
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
