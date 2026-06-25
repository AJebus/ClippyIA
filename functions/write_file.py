import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the content to a specific file declared in file_path, providing confirmation and ammount or characters written",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text that will be written inside the file at file_path",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        is_dir = os.path.isdir(target_file)
        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: writting to file: {e}"
