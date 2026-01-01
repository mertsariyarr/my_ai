from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content],
)