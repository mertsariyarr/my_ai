import os
import subprocess
def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

    if not valid_target:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python3", target_file]

    if args:
        command.extend(args)

    

    output = ""
    
    my_process = subprocess.run(command,capture_output=True, text=True, timeout=30)
    stdout = my_process.stdout
    stderr = my_process.stderr
    try:
        if my_process.returncode != 0:
            output += f"\nProcess exited with code {my_process.returncode}"
        if stdout == "" or stderr == "":
            output += f"\nSTDOUT: {stdout}\nSTDERR: {stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"


   


            





