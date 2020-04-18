import subprocess
import os
import glob
import argparse

IS_DEBUG = False

PROG_VERSION = "0.0.1 - Alpha"

def main():
    args = processArgs()
    dbg_print(args.is_debug, "Successfully parsed args")

    mergeAudio(args)


# Sets all the default values, and does basic work on args
def processArgs():
    args = parseArgs()

    if args.version:
        print (PROG_VERSION)
        return

    if args.num_parts:
        num_parts = args.num_parts
    else:
        args.num_parts = 4

    if not args.directory:
        args.directory = os.getcwd

    if args.is_debug:
        IS_DEBUG = True

    return args

def dbg_print(is_debug, *args, **kwargs):
    if is_debug is True:
        print(*args, **kwargs)


def mergeAudio(args):
    workingDir = os.getcwd()
    if args.recursive:
        workingFiles = os.path.join(workingDir, "**/*.mp3")
    else:
        workingFiles = os.path.join(workingDir, "*.mp3")

    dbg_print(args.is_debug, f"Started script at path {workingDir}")
    dbg_print(args.is_debug, f"Wildcard pattern is {workingFiles}")

    files = glob.glob(workingFiles)
    print(files)


# Parses command line args passed to the program
def parseArgs():
    parser = argparse.ArgumentParser(
        description="Merge many mp3 files into one"
    )

    help_texts = {
        "version": "output program version and exit.",
        "num_parts": "specify number of parts you want to split into. Default: 4",
        "directory": "specify where to run program. Default: wherever you call it.",
        "recursive": "specify that subdirs should be processed.",
        "debug"  : "start in debug mode. Prints text to follow program's flow."
    }

    parser.add_argument("-v", "--version",
                        action="store_true",
                        dest="version",
                        help=help_texts["version"])

    parser.add_argument("-n",
                        action="store",
                        dest="num_parts",
                        help=help_texts["num_parts"])

    parser.add_argument("-d",
                        action="store",
                        dest="directory",
                        help=help_texts["directory"])

    parser.add_argument("-r",
                        action="store_true",
                        dest="recursive",
                        help=help_texts["recursive"])

    parser.add_argument("--dbg",
                        action="store_true",
                        dest="is_debug",
                        help=help_texts["version"])

    return parser.parse_args()

if __name__ == "__main__":
    main()
