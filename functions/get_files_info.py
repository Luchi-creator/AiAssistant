import os

def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_path = os.path.abspath(os.path.join(working_directory, directory))

        # Check if path is within working_directory
        if not (abs_target_path == abs_working_dir or abs_target_path.startswith(abs_working_dir + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if target is a directory
        if not os.path.isdir(abs_target_path):
            return f'Error: "{directory}" is not a directory'

        items = os.listdir(abs_target_path)
        result_lines = []

        for item in sorted(items):  # Sorting for predictable output
            item_path = os.path.join(abs_target_path, item)
            try:
                size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                result_lines.append(f" - {item}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                result_lines.append(f" - {item}: Error retrieving info: {str(e)}")

        # Customize heading for "." and subdirectories
        if directory == ".":
            heading = "Result for current directory:"
        else:
            heading = f"Result for '{directory}' directory:"

        return f"{heading}\n" + "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"
