import os
def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if not valid_target:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    if directory == ".":
        item_list = "Result for current directory:\n"
    else:
        item_list = f"Result for {directory} directory:\n"
    
    for item in os.listdir(target_dir):
        if item == "__pycache__":
            continue
        item_list += f"- {item}: file_size={os.path.getsize(target_dir + "/" + item)} bytes, is_dir={os.path.isdir(target_dir + "/" + item)}\n"
    
    return item_list


    
    