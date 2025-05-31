from google.genai import types


def run_python_file(working_directory, file_path):
    """
    Run a Python file within the specified working directory.
    
    Args:
        working_directory (str): The base directory to ensure the file is within.
        file_path (str): The path to the Python file relative to the working directory.
        
    Returns:
        str: The output of the Python script or an error message if the file is outside the working directory.
    """
    import os
    import subprocess

    # Ensure the file path is within the working_directory
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_path = os.path.abspath(working_directory)

    if not absolute_file_path.startswith(working_directory_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: File "{file_path}" not found.'
    if not absolute_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        result = subprocess.run(
            ['python', absolute_file_path],
            cwd=working_directory,
            timeout=30,
            capture_output=True,
            text=True
        )
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        if result.returncode != 0:
            return (
                f"STDOUT:\n{stdout}\n"
                f"STDERR:\n{stderr}\n"
                f"Process exited with code {result.returncode}"
            )
        elif stdout or stderr:
            return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        else:
            return "No output produced."

    except subprocess.TimeoutExpired:
        return "Error: Execution timed out."
    except subprocess.CalledProcessError as e:
        return f"Error: Failed to execute Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Runs a Python file within the specified working directory, ensuring it is within the allowed directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to run the Python file from, relative to the working directory.",
                ),
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The name of the Python file to run.",
                ),
            },
        ),
    )