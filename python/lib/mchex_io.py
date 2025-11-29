import os
import typing


def do_sources(place_directory: str, do_func: typing.Callable[[str], None]):
    with os.scandir(place_directory) as entries:
        for entry in entries:
            if entry.is_file():
                continue
            do_func(os.path.join(entry.path, "src"))
    return


def get_sources(place_directory: str):
    result = []
    do_sources(place_directory, lambda path: result.append(path))
    return result
