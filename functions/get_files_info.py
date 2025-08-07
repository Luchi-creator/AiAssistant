import os
import subprocess
from google import genai
from google.genai import types
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
    

def run_python_file(working_directory, file_path, args=[]):
    try:
        abs_working_path = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory,file_path))
        
        if not(abs_file_path == abs_working_path or abs_file_path.startswith(abs_working_path + os.sep)):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        command = ["python3", abs_file_path]
        if args:  # Only add args if they exist
            command.extend(args)

        completed_process = subprocess.run(command, capture_output=True, timeout=30, cwd=working_directory) 
        result = f"STDOUT: {completed_process.stdout.decode() if completed_process.stdout else ""}\nSTDERR: {completed_process.stderr.decode() if completed_process.stderr else ""}"
                
        if completed_process.returncode != 0:
            result += f"\n Process exited with code {completed_process.returncode}"

        if completed_process.stdout == None:
            return "No output produced"
        
        return result
        
    except Exception as e:
        return f"Error: executing Python file: {e}"
    


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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file within the working directory. If the file is too large, the content is truncated at 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base working directory. Only files within this directory can be accessed."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory."
            ),
        },
        required=["working_directory", "file_path"]
    )
)



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and captures stdout and stderr output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base working directory. Only files within this directory can be executed."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory."
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of command-line arguments to pass to the script."
            ),
        },
        required=["working_directory", "file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates directories as needed.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "working_directory": types.Schema(
                type=types.Type.STRING,
                description="The base working directory. The file must be inside this directory."
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file."
            ),
        },
        required=["working_directory", "file_path", "content"]
    )
)

