from google.genai import types
from functions.get_files_info import *

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)