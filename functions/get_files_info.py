import os
from functions.config import MAX_CHARS

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(working_directory, directory))

        if not (abs_target_path == abs_working_dir or abs_target_path.startswith(abs_working_dir + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target_path):
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(abs_target_path)
        result_lines = []

        for item in sorted(items): 
            item_path = os.path.join(abs_target_path, item)
            try:
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                result_lines.append(f" - {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                result_lines.append(f" - {item}: Error retrieving info: {str(e)}")

        if directory == ".":
            heading = "Result for current directory:"
        else:
            heading = f"Result for '{directory}' directory:"

        return f"{heading}\n" + "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"


def get_file_content(working_directory, file_path):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))

        if not(abs_file_path == abs_working_path or abs_file_path.startswith(abs_working_path + os.sep)):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        MAX_CHARS = 10000

        with open(abs_file_path, "r") as f:
            file_content_string = f.read()
        
        if len(file_content_string) > MAX_CHARS:
            file_content_string = file_content_string[0:10000]
            file_content_string += '[...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        return f"Error: {str(e)}"
    

def write_file(working_directory, file_path, content):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
        dir_file_path = os.path.dirname(abs_file_path)

        if not(abs_file_path == abs_working_path or abs_file_path.startswith(abs_working_path + os.sep)):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
        if not os.path.exists(abs_working_path):
            os.makedirs(dir_file_path)

        with open(abs_file_path, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"
    