import subprocess
import os
import argparse

prog_version = "0.0.1 - Alpha"

def main():
    args = parseArgs()
    if args.version:
        print (prog_version)
        return
    if args.num_parts:
        num_parts = args.num_parts
    else:
        args.num_parts = 4


# Parses command line args passed to the program
def parseArgs():
    parser = argparse.ArgumentParser(
        description="Merge many mp3 files into one"
    )

    help_texts = {
        "version": "Output program version and exit.",
        "num_parts": "Specify number of parts you want to split into. Default: 4",
        "debug"  : "Start in debug mode."
    }

    parser.add_argument("-v", "--version",
                        action="store_true",
                        dest="version",
                        help=help_texts["version"])

    parser.add_argument("-n",
                        action="store",
                        dest="num_parts",
                        help=help_texts["num_parts"])

    parser.add_argument("--dbg",
                        action="store_true",
                        dest="is_debug",
                        help=help_texts["version"])

    return parser.parse_args()

if __name__ == "__main__":
    main()