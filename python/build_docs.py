import os
import sys
import argparse
import subprocess
import lib.mchex_io as mchexio

if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        "Build Docs", description="Builds the Moonwave docs"
    )

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
    PARSER.add_argument(
        "--publish", "-P", action="store_true", help="Publishes to the web"
    )

    ARGS = PARSER.parse_args()

    try:
        subprocess.run("moonwave --help", stdout=subprocess.PIPE, timeout=1, check=True)
    except subprocess.TimeoutExpired as e:
        print(f"Moonwave took too long to respond!")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Fail to run Moonwave")
        sys.exit(1)

    assert os.path.isdir(ARGS.places), "Invalid places directory!"

    if ARGS.publish:
        subprocess.run(
            f"moonwave build --publish --code {mchexio.get_sources(ARGS.places)} --out-dir {ARGS.out_dir}"
        )
        sys.exit(0)

    if ARGS.dev:
        subprocess.run(
            f"moonwave dev --code {mchexio.get_sources(ARGS.places)} --out-dir {ARGS.out_dir}"
        )
        sys.exit(0)

    try:
        subprocess.run(
            f"moonwave build --code {mchexio.get_sources(ARGS.places)} --out-dir {ARGS.out_dir}",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Moonwave could not generate docs! There are errors!")
        sys.exit(1)
sys.exit(0)
