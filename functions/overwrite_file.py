from google.genai import types

def overwrite_file(working_directory, file_path, content):
    """
    Overwrite the content of a file within the working directory.
    
    Args:
        working_directory (str): The base directory to ensure the file is within.
        file_path (str): The path to the file relative to the working directory.
        content (str): The new content to write to the file.
        
    Returns:
        str: A success message or an error message if the file is outside the working directory or cannot be written.
    """
    import os
    
    absolute_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    working_directory_path = os.path.abspath(working_directory)

    if not absolute_file_path.startswith(working_directory_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        with open(absolute_file_path, 'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} bytes written)'
    except Exception as e:
        return f'Error writing to file: {e}'
    
schema_overwrite_file = types.FunctionDeclaration(
        name="overwrite_file",
        description="Overwrites a file with new content, ensuring the file is within the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to overwrite, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    )