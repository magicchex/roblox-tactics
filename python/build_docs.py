import os
import sys
import argparse
import subprocess

PARSER = argparse.ArgumentParser("Build Docs", description="Builds the Moonwave docs")

PARSER.add_argument(
    "--places",
    "-p",
    default="places",
    help="The directory containing all of your Rojo projects",
)
PARSER.add_argument(
    "--out-dir", "-o", default="out/moonwave", help="The output directory"
)
PARSER.add_argument("--dev", "-d", action="store_true", help="Enables live-reload")
PARSER.add_argument("--publish", "-P", action="store_true", help="Publishes to the web")

ARGS = PARSER.parse_args()

try:
    m = subprocess.run("moonwave help", stdout=subprocess.PIPE, timeout=1, check=True)
except subprocess.TimeoutExpired as e:
    print(f"{e.with_traceback()}\n\nMoonwave took too long to respond!")
    sys.exit(1)
except subprocess.CalledProcessError as e:
    print(f"{e.with_traceback()}\n\nFail to run Moonwave")
    sys.exit(1)

assert os.path.isdir(ARGS.places), "Invalid places directory!"

sources = ""
with os.scandir(ARGS.places) as entries:
    for entry in entries:
        if entry.is_file():
            continue
        sources += f'"{os.path.join(entry.path, "src")}",'
sources = sources.removesuffix(",")

if ARGS.publish:
    moonwave = subprocess.run(f"moonwave build --publish --code [{sources}]")
    sys.exit(0)

if ARGS.dev:
    moonwave = subprocess.run(
        f"moonwave dev --code [{sources}] --out-dir {ARGS.out_dir}"
    )
    sys.exit(0)

try:
    moonwave = subprocess.run(
        f"moonwave build --code [{sources}] --out-dir {ARGS.out_dir}", check=True
    )
except subprocess.CalledProcessError as e:
    print(
        f"{e.with_traceback()}\n\nMoonwave could not generate docs! There are errors!"
    )
    sys.exit(1)
sys.exit(0)
