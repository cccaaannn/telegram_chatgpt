import pathlib
import os


class FileUtils:

    @staticmethod
    def create_abs_aware_parent_dir(full_path: str) -> str:
        splitted_full_path = os.path.split(full_path)
        filename = splitted_full_path[1]
        path = splitted_full_path[0]
        if(not os.path.isabs(path)):
            path = os.path.join(os.getcwd(), path)
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return os.path.join(path, filename)
