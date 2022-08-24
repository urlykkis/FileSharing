import os
import zipfile


async def zipdir(path: str) -> list[list[str]]:
    dir_files: list = []

    for root, dirs, files in os.walk(path):
        for file in files:
            dir_files.append([os.path.join(root, file),
                              os.path.relpath(os.path.join(root, file), os.path.join(path, '..'))])
    return dir_files


async def archive_directory(path_to_save: str, path_to_dir: str) -> str:
    dir_files: list = await zipdir(path_to_dir)

    if not os.path.exists(path_to_save):
        with zipfile.ZipFile(path_to_save, 'w', zipfile.ZIP_DEFLATED, True) as zipf:
            for file in dir_files:
                zipf.write(file[0], file[1])

    return path_to_dir
