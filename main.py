import subprocess
import os
import glob
import argparse

PROG_VERSION = "0.0.1 - Alpha"

def main():
    args = processArgs()
    dbg_print(args.is_debug, "Successfully parsed args")

    mergeAudio(args)


# Sets all the default values, and does basic work on args
def processArgs():
    args = parseArgs()

    if args.version:
        print(PROG_VERSION)
        return

    if args.numParts:
        numParts = args.numParts
    else:
        args.numParts = 4

    if not args.directory:
        args.directory = os.getcwd

    return args


def dbg_print(is_debug, *args, **kwargs):
    if is_debug is True:
        print(*args, **kwargs)


def mergeAudio(args):
    files = getFiles(args)
    fileConcatStrings = getConcatStrings(files)
    if not args.yes:
        confirmation = input("This is how the files will be merged. Proceed? (y/n) ")
        if confirmation != "y":
            print("Aborting...")
            return

    if args.outputName:
        outputName = args.fileName
    else:
        outputName = "output"

    dbg_print(args.is_debug, "Merging files...")
    mergeFiles(outputName, fileConcatStrings)


def mergeFiles(outputName, fileConcatStrings):
    counter = 0
    for i in fileConcatStrings:
        counter += 1
        # os.system(f"ffmpeg -i \"concat:{i}\" -acodec copy {outputName}{counter}.mp3")
        print(f"ffmpeg -i \"concat:{i}\" -acodec copy {outputName}{counter}.mp3")


def getConcatStrings(files):
    fileConcatStrings = []
    for i in files:
        fileConcatString = "|".join(i)
        fileConcatStrings.append(fileConcatString)
        print(fileConcatString)
    return fileConcatStrings


def getFiles(args):
    workingDir = os.getcwd()
    if args.recursive:
        workingFiles = os.path.join(workingDir, "**/*.mp3")
    else:
        workingFiles = os.path.join(workingDir, "*.mp3")

    dbg_print(args.is_debug, f"Started script at path {workingDir}")
    dbg_print(args.is_debug, f"Wildcard pattern is {workingFiles}")

    files = sorted(glob.glob(workingFiles))

    files = splitFiles(files, args.numParts)

    return files


def splitFiles(files, numParts):
    splitFiles = []
    fileNum = len(files)

    if fileNum <= numParts:
        print(f"You don't have enough files for {numParts} parts!")
        quit()

    remainder = fileNum%numParts
    fileNum -= remainder
    # Int conversion necessary; else it becomes a float, no idea why
    partSize = int(fileNum / numParts)

    for i in range(numParts):
        startPoint = i * partSize
        endPoint = startPoint + partSize
        buff = files[startPoint:endPoint]
        splitFiles.append(buff)

    # Remainder gets added onto last part
    for i in range(fileNum + 1, fileNum + remainder):
        splitFiles[-1].append(files[i])

    return splitFiles


# Parses command line args passed to the program
def parseArgs():
    parser = argparse.ArgumentParser(
        description="Audiomerger - Merge many mp3 files into bigger parts"
    )

    help_texts = {
        "version": "output program version and exit.",
        "numParts": "specify number of parts you want to split into. default: 4",
        "name": "Specify name of output files. This + number + .mp3 is final name.",
        "directory": "specify where to run program. default: wherever you call it.",
        "yes": "skip prompts which ensure you got the right files.",
        "delete": "delete the files you merged in after completion.",
        "recursive": "specify that subdirs should be processed. note: broken",
        "debug"  : "start in debug mode. prints text to follow program's flow."
    }

    parser.add_argument("-v", "--version",
                        action="store_true",
                        dest="version",
                        help=help_texts["version"])

    parser.add_argument("-n",
                        action="store",
                        type=int,
                        dest="numParts",
                        help=help_texts["numParts"])

    parser.add_argument("-a",
                        action="store",
                        dest="outputName",
                        help=help_texts["name"])

    parser.add_argument("-d",
                        action="store",
                        dest="directory",
                        help=help_texts["directory"])

    parser.add_argument("-y",
                        action="store_true",
                        dest="yes",
                        help=help_texts["yes"])

    parser.add_argument("-r",
                        action="store_true",
                        dest="recursive",
                        help=help_texts["recursive"])

    parser.add_argument("--delete",
                        action="store_true",
                        dest="delete",
                        help=help_texts["delete"])

    parser.add_argument("--dbg",
                        action="store_true",
                        dest="is_debug",
                        help=help_texts["debug"])

    return parser.parse_args()

if __name__ == "__main__":
    main()
