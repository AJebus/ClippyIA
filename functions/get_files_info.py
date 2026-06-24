import os


def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        valid_directory = os.path.isdir(target_dir)
        if not valid_directory:
            return f'Error: "{directory}" is not a directory'

        files_list: list[str] = []
        files_list.append(f"Result for {target_dir} directory:")
        for file in os.listdir(target_dir):
            target_file = os.path.normpath(os.path.join(target_dir, file))
            name: str = file
            file_size: int = os.path.getsize(target_file)
            is_dir: bool = os.path.isdir(target_file)
            files_list.append(
                f"  - {name}: file_size={file_size} bytes, is_dir={is_dir}"
            )

        return "\n".join(files_list)
    except Exception as e:
        return f"Error: {e}"
