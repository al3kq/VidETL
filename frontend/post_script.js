
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('jsonForm');
    const addTaskBtn = document.getElementById('addTaskBtn');
    const tasksContainer = document.getElementById('tasks');
    const outputJSON = document.getElementById('outputJSON');

    function createTaskInputs(taskType) {
        // Same function as before for creating task inputs
    }

    addTaskBtn.addEventListener('click', function() {
        // Same event listener as before for adding tasks
    });

    tasksContainer.addEventListener('change', function(e) {
        // Same event listener as before for handling task type change
    });

    tasksContainer.addEventListener('click', function(e) {
        // Same event listener as before for removing tasks
    });

    form.addEventListener('submit', function(e) {
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
            // Same logic as before for gathering task data
        });

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
