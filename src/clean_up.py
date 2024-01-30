import subprocess
import os

def clean_up():
    def execute_bash_script():
        cltemp = "cltemp"
        # Get the current directory of the Python script
        dir_path = os.path.dirname(os.path.realpath(__file__))

        # Construct the full path of the Bash script
        script_path = os.path.join(dir_path, script_name)

        # Check if the script file exists
        if not os.path.isfile(script_path):
            print(f"Script not found: {script_path}")
            return

        # Execute the script
        try:
            result = subprocess.run(['bash', script_path], check=True, text=True, capture_output=True)
            print("Script output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Error occurred while executing the script:", e)

    # Example usage
    execute_bash_script('clout.sh')
    execute_bash_script('cltemp.sh')
