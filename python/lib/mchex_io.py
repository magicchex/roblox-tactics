import os
import typing
import json
import sys


class ProjectID(typing.TypedDict):
    universe_id: int | None
    place_id: int | None


class NoGameID(Exception):
    pass


class NoPlaceID(Exception):
    pass


class UntitledProject(Exception):
    pass


def do_projects(place_directory: str, do_func: typing.Callable[[str], None]):
    with os.scandir(place_directory) as entries:
        for entry in entries:
            if entry.is_file():
                continue
            do_func(entry.path)
    return


def get_projects(place_directory: str) -> list[str]:
    result = []
    do_projects(place_directory, lambda path: result.append(path))
    return result


def do_sources(place_directory: str, do_func: typing.Callable[[str], None]):
    def s(path):
        do_func(os.path.join(path, "src"))

    do_projects(place_directory, s)


def get_sources(place_directory: str) -> list[str]:
    result = []
    do_sources(place_directory, lambda path: result.append(path))
    return result


def get_project_ids(project_json_path: str) -> ProjectID:
    with open(project_json_path, "r") as f:
        j_content: dict = json.loads(f.read())
    result: ProjectID = {
        "universe_id": j_content.get("gameId"),
        "place_id": j_content.get("placeId"),
    }
    if result["universe_id"] is None:
        raise NoGameID("Rojo Project does not have an defined gameId!")
    if result["place_id"] is None:
        raise NoPlaceID("Rojo Project does not have an defined placeId!")
    return result


def get_project_name(project_json_path: str):
    with open(project_json_path, "r") as f:
        j_content: dict = json.loads(f.read())
    result: str = j_content.get("name")
    if result is None:
        raise UntitledProject("Rojo Project does not have an defined name!")
    return result
