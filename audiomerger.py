#!/usr/bin/python3
import subprocess
import os
import re
import glob
import argparse

PROG_VERSION = "1.0.0 - Final"

def main():
    args = processArgs()

    mergeAudio(args)


# Sets all the default values, and does basic work on args
def processArgs():
    args = parseArgs()

    if args.version:
        print(PROG_VERSION)
        quit()

    if args.numParts:
        numParts = args.numParts
    else:
        args.numParts = 4

    if not args.directory:
        args.directory = os.getcwd()
    
    if not args.outputName:
        args.outputName = os.path.basename(args.directory)
    
    return args


def mergeAudio(args):
    files = getFiles(args)
    fileConcatStrings = getConcatStrings(files)
    if not args.yes:
        confirmation = input(f"{color.RED}This is how the files will be merged. Proceed? (y/n){color.END} ")
        if confirmation != "y":
            print(f"{color.RED}Aborting...{color.END}")
            return

    mergeFiles(args.outputName, fileConcatStrings)
    if(args.delete):
        for filecat in files:
            for filen in filecat:
                os.remove(filen)
                # print(filen)


def mergeFiles(outputName, fileConcatStrings):
    counter = 0
    for i in fileConcatStrings:
        counter += 1
        os.system(f"ffmpeg -loglevel error -i \"concat:{i}\" -acodec copy {outputName}{counter}.mp3")
        # print(f"ffmpeg -i \"concat:{i}\" -acodec copy {outputName}{counter}.mp3")


def getConcatStrings(files):
    fileConcatStrings = []
    for i in files:
        fileConcatString = "|".join(i)
        fileConcatStrings.append(fileConcatString)
        print(fileConcatString)
    return fileConcatStrings


def getFiles(args):
    if args.recursive:
        workingFiles = os.path.join(args.directory, "**/*.mp3", recursive=True)
    else:
        workingFiles = os.path.join(args.directory, "*.mp3")

    files = naturalSort(glob.glob(workingFiles))

    files = splitFiles(files, args.numParts)

    return files


def naturalSort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def splitFiles(files, numParts):
    splitFiles = []
    fileNum = len(files)

    if fileNum <= numParts:
        print(f"{color.RED}You don't have enough files for {numParts} parts!{color.END}")
        quit()

    remainder = fileNum%numParts
    fileNum -= remainder
    # Int conversion necessary, else it becomes a float; no idea why
    partSize = int(fileNum / numParts)

    for i in range(numParts):
        startPoint = i * partSize
        endPoint = startPoint + partSize
        buff = files[startPoint:endPoint]
        splitFiles.append(buff)

    # Remainder gets added onto last part
    for i in range(fileNum, fileNum + remainder):
        splitFiles[-1].append(files[i])

    return splitFiles


# Parses command line args passed to the program
def parseArgs():
    parser = argparse.ArgumentParser(
        description="Audiomerger - Merge many mp3 files into bigger parts",
        epilog=f"{color.BOLD}NOTE: DO NOT USE SPACES IN ANY ARGUMENTS{color.END}"
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

    return parser.parse_args()

# Credits for this class go to https://stackoverflow.com/questions/8924173/how-do-i-print-bold-text-in-python
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

if __name__ == "__main__":
    main()
