import os
import sys
import argparse
import subprocess
import lib.mchex_io as mchexio


def style_documents(path: str):
    try:
        subprocess.run(
            f"stylua {path}",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f'\n\nStylua couldn\'t stylize document, "{path}"!')
    return


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("Stylua", description="Stylizes Lua documents")

    PARSER.add_argument(
        "--places",
        "-p",
        default="places",
        help="The directory containing all of your Rojo projects",
    )

    ARGS = PARSER.parse_args()

    try:
        subprocess.run("stylua --help", stdout=subprocess.PIPE, timeout=1, check=True)
    except subprocess.TimeoutExpired as e:
        print(f"{e.with_traceback()}\n\nStylua took too long to respond!")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"{e.with_traceback()}\n\nFail to run Stylua")
        sys.exit(1)

    assert os.path.isdir(ARGS.places), "Invalid places directory!"

    mchexio.do_sources(ARGS.places, style_documents)
sys.exit(0)
