import os
from google.genai import types

def get_file_content(working_directory, file_path):
    """
    Get the content of a file within the working directory.
    
    Args:
        working_directory (str): The base directory to ensure the file is within.
        file_path (str): The path to the file relative to the working directory.
        
    Returns:
        str: The content of the file or an error message if the file is outside the working directory.
    """
    # Ensure the file path is within the working_directory
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_path = os.path.abspath(working_directory)

    if not absolute_file_path.startswith(working_directory_path):
        f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        f'Error: File not found or is not a regular file: "{file_path}"'

    # If the file is longer than 10000 characters, truncate it to 10000 characters and append this message to the end:
    if os.path.getsize(absolute_file_path) > 10000:
        with open(absolute_file_path, 'r') as file:
            try:
                content = f"{file.read(10000)} [...File {file_path} truncated at 10000 characters]"
            except Exception as e:
                return f'Error reading file: {e}'
            return content

    with open(absolute_file_path, 'r') as file:
        try:
            content = file.read()
        except Exception as e:
            return f'Error reading file: {e}'

    return content

schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Retrieves the content of a file, ensuring it is within the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
        ),
    )