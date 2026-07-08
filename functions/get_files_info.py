import os

# - README.md: file_size=1032 bytes, is_dir=False
# - src: file_size=128 bytes, is_dir=True
# - package.json: file_size=1234 bytes, is_dir=False

def get_files_info(working_directory: str, sub_dir='.'):

    abs_working_dir = os.path.abspath(working_directory)
    abs_dir = os.path.abspath(os.path.join(working_directory, sub_dir))
    if not abs_dir.startswith(abs_working_dir):
        return f"Error: {sub_dir} is not in a working dir"

    final_response = ''
    contents = os.listdir(abs_dir)
    for content in contents:
        content_path = os.path.join(abs_dir, content)
        is_dir = os.path.isdir(content_path)
        size = os.path.getsize(content_path)
        final_response += f'- {content}: file_size={size} bytes, is_dir={is_dir}\n'
    return final_response
