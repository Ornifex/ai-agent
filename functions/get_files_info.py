import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    """
    Get information about files in a directory within the working directory.

    Args:
        working_directory (str): The base directory to ensure the files are within.
        directory (str, optional): The subdirectory to list files from. Defaults to None, which means the working_directory itself.

    Returns:
        str: A string containing the names, sizes, and types of files in the specified directory.
    """
    # Ensure the directory is within the working_directory
    if directory:
        directory_path = os.path.abspath(os.path.join(working_directory, directory))
        working_directory_path = os.path.abspath(working_directory)

        if not directory_path.startswith(working_directory_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(directory_path):
            return f'Error: "{directory}" is not a directory'
    else:
        directory_path = os.path.abspath(working_directory)

    # Build a string representing the contents of the directory
    files_info = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        file_size = os.path.getsize(file_path) if os.path.isfile(file_path) else 0
        is_dir = os.path.isdir(file_path)
        files_info.append(f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}")

    return "\n".join(files_info) if files_info else "No files found in the specified directory."

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
