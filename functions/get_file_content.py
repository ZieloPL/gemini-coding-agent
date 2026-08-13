import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f"Error: {file_path} is not in a working dir"
    if not os.path.isfile(abs_file_path):
        return f"Error: {file_path} is not in a file"

    file_content = ''
    try:
        with open(abs_file_path, 'r') as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) >= MAX_CHARS:
                file_content += (
                    f'[...File {file_path} truncated at 10000 characters]'
                )
        return file_content
    except Exception as e:
        return f'Exception reading file {file_path}: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name='get_file_content',
    description='Gets the content of the given file as the string, constrained to the working directory.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, from the working directory.",
            )
        }
    )
)


