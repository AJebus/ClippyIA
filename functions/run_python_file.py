import os
import subprocess


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
            command, capture_output=True, text=True, timeout=30
        )

        output: str = ""
        return_code = completed_process.returncode
        if return_code != 0:
            output += f"Process exited with code {return_code}"
        if completed_process.stderr is None and completed_process.stdout is None:
            output += "No output produced"
        else:
            if completed_process.stdout is not None:
                output += f"STDOUT: {completed_process.stdout}"
            if completed_process.stderr is not None:
                output += f"STDERR: {completed_process.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
