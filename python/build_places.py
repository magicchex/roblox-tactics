import os
import sys
import argparse
import subprocess
import json
import lib.mchex_io as mchexio


if __name__ == "__main__":
    DEFAULT_PROJECT = "default.project.json"
    FILE_EXT = ".rbxl"
    DOT_VSCODE = os.path.join(".vscode", "settings.json")
    DOT_VSCODE_INDENT = 2
    LUAU_ROJO_SETTING = "luau-lsp.sourcemap.rojoProjectFile"
    PARSER = argparse.ArgumentParser("Build Places", description="Builds Roblox Places")

    PARSER.add_argument(
        "--places",
        "-p",
        default="places",
        help="The directory containing all of your Rojo projects",
    )
    PARSER.add_argument(
        "--out-dir", "-o", default=r"out\places", help="The output directory"
    )
    PARSER.add_argument("--dev", "-d", action="store_true", help="Enables live-reload")
    PARSER.add_argument(
        "--publish",
        "-P",
        default=None,
        help="Publishes to Roblox using the given API KEY",
    )

    ARGS = PARSER.parse_args()

    try:
        subprocess.run("rojo --help", stdout=subprocess.PIPE, timeout=1, check=True)
    except subprocess.TimeoutExpired as e:
        print(f"Rojo took too long to respond!")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Fail to run Rojo")
        sys.exit(1)

    assert os.path.isdir(ARGS.places), "Invalid places directory!"
    if not os.path.isdir(ARGS.out_dir):
        os.makedirs(ARGS.out_dir, exist_ok=True)
    if not os.path.isdir(os.path.join(DOT_VSCODE, os.pardir)):
        os.makedirs(os.path.join(DOT_VSCODE, os.pardir))

    def build_place(path: str):
        global ARGS
        project_path = os.path.join(path, DEFAULT_PROJECT)
        try:
            project_name = mchexio.get_project_name(project_path)
            project_ids = mchexio.get_project_ids(project_path)
        except mchexio.UntitledProject as e:
            print(e.args[0])
            return
        except mchexio.NoGameID as e:
            print(e.args[0])
            return
        except mchexio.NoPlaceID as e:
            print(e.args[0])
            return
        project_name += f" ({project_ids['place_id']})"
        if ARGS.publish is not None:
            try:
                subprocess.run(
                    f'rojo upload --api_key "{ARGS.publish}" --universe_id {project_ids['universe_id']} --asset_id {project_ids['place_id']} "{project_path}"',
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f'Rojo faced an issue when publishing place, "{project_path}"!')
            return
        try:
            subprocess.run(
                f'rojo build -o "{os.path.join(ARGS.out_dir,project_name+FILE_EXT)}" "{project_path}"',
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(f'Rojo faced an issue when building place, "{project_path}"!')

    if ARGS.dev:

        def i(projects: list[str]):
            answer = "-1"
            try:
                while int(answer) < 0 or int(answer) >= len(projects):
                    for choice, project in enumerate(projects):
                        print(f"[{choice}]\t{project.split(os.sep)[-1]}")
                    answer = input()
            except ValueError:
                i(projects)
            return int(answer)

        projects = mchexio.get_projects(ARGS.places)
        selected_project = os.path.join(projects[i(projects)], DEFAULT_PROJECT)
        name = mchexio.get_project_name(selected_project)
        ids = mchexio.get_project_ids(selected_project)
        name += f" ({ids['place_id']})"
        selected_project = selected_project.replace(os.sep, "/")
        if not os.path.isfile(DOT_VSCODE):
            with open(DOT_VSCODE, "x") as f:
                f.write(json.dumps({}, indent=DOT_VSCODE_INDENT))
        with open(DOT_VSCODE, "r") as f:
            vs_content: dict = json.loads(f.read())
        vs_content[LUAU_ROJO_SETTING] = selected_project
        with open(DOT_VSCODE, "w") as f:
            f.write(json.dumps(vs_content, indent=DOT_VSCODE_INDENT))
        subprocess.run(f'rojo serve "{selected_project}"')
        sys.exit(0)

    mchexio.do_projects(ARGS.places, build_place)

sys.exit(0)
