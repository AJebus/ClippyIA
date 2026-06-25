import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the python program found at the file_path and feeds it the arguments in args, provides the output of the program as well as the error codes if any",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the python program to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments that will be fed to the program, if none are required defaults to None",
            ),
        },
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        valid_target_file = (
            os.path.commonpath([abs_working_dir, abs_file_path]) == abs_working_dir
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        is_file = os.path.isfile(abs_file_path)
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", abs_file_path]
        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output: list[str] = []
        return_code = completed_process.returncode
        if return_code != 0:
            output.append(f"Process exited with code {return_code}")
        if completed_process.stderr is None and completed_process.stdout is None:
            output.append("No output produced")
        else:
            if completed_process.stdout is not None:
                output.append(f"STDOUT: {completed_process.stdout}")
            if completed_process.stderr is not None:
                output.append(f"STDERR: {completed_process.stderr}")

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
