#!/usr/bin/env python3

from termcolor import colored
from colorama import init
from PIL import Image
from PyPDF2 import PdfFileMerger
from pathlib import Path
import platform
import os

jpg_files = []
pdf_files = []
text = "green"


def linux_path(file): # Parse file path for Linux based OS
        linux_user = os.getlogin()

        if file.startswith('/') or file.endswith('/'):
            path = file.strip('/')

        if linux_user == 'root':
            path = os.path.join(os.path.expanduser('~'), file)
        else:
            path = os.path.abspath('/home/' + linux_user + '/' + file)

        return path


def compare_file(file, isLinux): # Before adding to the list of files to convert, we need to check it
    while True:
        try:
            if file in jpg_files:
                if not isLinux:
                    file = input("\nYou have already chosen that file. Enter path of another JPEG file to convert: ")
                else:
                    file = input(colored("\nYou have already chosen that file. Enter path of another JPEG file to convert: ", text))
                    file = linux_path(file)
            elif not Path(file).is_file():
                if not isLinux:
                    file = input("\nFile not found. Enter path of JPEG file to convert: ")
                else:
                    file = input(colored("\nFile not found. Enter path of JPEG file to convert: ", text))
                    file = linux_path(file)
            elif not file.lower().endswith(('.png', '.jpg', '.jpeg')):
                if not isLinux:
                    file = input("\nInvalid file. Enter path of JPEG file to convert: ")
                else:
                    file = input(colored("\nInvalid file. Enter path of JPEG file to convert: ", text))
                    file = linux_path(file)
            elif os.stat(file).st_size == 0:
                if not isLinux:
                    file = input("\nFile empty. Enter path of JPEG file to convert: ")
                else:
                    file = input(colored("\nFile empty. Enter path of JPEG file to convert: ", text))
                    file = linux_path(file)
            else:
                jpg_files.append(file)
                break
        except KeyboardInterrupt:
            print('\n')
            return


def add_more_files(isLinux): # After adding of initial file, check if more files are to be added
    while True:
        try:
            if not isLinux:
                addFile = input("\nAdd another file? (y/n): ")
            else:
                addFile = input(colored("\nAdd another file? (y/n): ", text))

            while True:
                if not addFile.lower() in {'y', 'n'}:
                    if not isLinux:
                        addFile = input("\nEnter y or n: ")
                    else:
                        addFile = input(colored("\nEnter y or n: ", text))
                elif addFile.lower() == 'n':
                    return
                elif addFile.lower() == 'y':
                    if not isLinux:
                        file_check = input("\nEnter path of JPEG/PNG file to convert: ")
                        compare_file(file_check, isLinux)
                    else:
                        file_check = input(colored("\nEnter path of JPEG/PNG file to convert: ", text))
                        linuxFilePath = linux_path(file_check)
                        compare_file(linuxFilePath, isLinux)
                    break
        except KeyboardInterrupt:
            print('\n')
            return


def main():
    isLinux = False

    if platform.system() == 'Linux':
        isLinux = True

    if not isLinux:
        init() # Color print() for Windows, import Colorama. If Linux is running then use TermColor

    print(colored("\t_______________________________________", text))
    print(colored("\n\t\t        JPEG2PDF", text))
    print(colored("\t\tv0.1. by: Pattros", text))
    print(colored("\t_______________________________________", text))

    try:
        if not isLinux:
            file_check = input("\nEnter path of JPEG/PNG file to convert: ")
        else:
            file_check = input(colored("\nEnter path of JPEG/PNG file to convert: ", text))
    except KeyboardInterrupt:
        print('\n')
        raise SystemExit

    if isLinux: # We need to parse the path entered by the user if Linux is running. Windows is ok
        linuxFilePath = linux_path(file_check)
        compare_file(linuxFilePath, isLinux)
    else:
        compare_file(file_check, isLinux)

    if not len(jpg_files) == 0: # Proceed only if user has selected file(s)
        add_more_files(isLinux)

        try: # After files have been selected for conversion, select a path where they will be stored
            if not isLinux:
                new_filename_path = input("\nEnter path to store file(s): ")
            else:
                new_filename_path = input(colored("\nEnter path to store file(s): ", text))
            if isLinux:
                new_filename_path = linux_path(new_filename_path)
        except KeyboardInterrupt:
            print('\n')
            raise SystemExit

        while True:
            try: # Keep prompting the user for a valid file path if it does not exist
                if not Path(new_filename_path).is_dir():
                    if not isLinux:
                        new_filename_path = input("\nFile path does not exist. Enter path to store file(s): ")
                    else:
                        new_filename_path = input(colored("\nFile path does not exist. Enter path to store file(s): ", text))
                    if isLinux:
                        new_filename_path = linux_path(new_filename_path)
                else:
                    break
            except KeyboardInterrupt:
                print('\n')
                raise SystemExit
    else:
        print('\n')
        raise SystemExit

    img_size = {}
    for file in jpg_files:
        img = Image.open(file)  # open each of the files
        img_size[Path(img.filename).name] = img.size  # store file size in img_size{}

    min_img_size = max(img_size.values())  # find file with the smallest size. This will be used to resize all the files later

    counter = 0
    try:
        for file in jpg_files: # this time open each of the files again, resize all to one size and save each in pdf format
            counter = counter + 1
            img = Image.open(file)
            new_img = img.resize((min_img_size[0], min_img_size[1]))

            if new_img.mode == "RGBA":
                new_img = new_img.convert("RGB")

            if not new_filename_path.endswith('/'):
                new_filename_path = new_filename_path + '/'

            new_filename = new_filename_path + "doc" + str(counter) + ".pdf"
            pdf_files.append(new_filename)
            new_img.save(new_filename, "PDF", resolution=100.0)
    except OSError as e: # throw error if for example the file opened is corrupt
        print("\nError: "+ str(e))

    if len(jpg_files) > 1:  # option to merge multiple pdf files into one pdf file
        try:
            if not isLinux:        
                merge_multiple = input("\nWould you like to merge all the files into one pdf file? (y/n): ")
            else:
                merge_multiple = input(colored("\nWould you like to merge all the files into one pdf file? (y/n): ", text))
        except:
            print('\n')
            return

        while True:
            try:
                if merge_multiple.lower() not in ('y', 'n'):
                    if not isLinux:
                        merge_multiple = input("\nEnter y or n: ")
                    else:
                        merge_multiple = input(colored("\nEnter y or n: ", text))
                elif merge_multiple.lower() == 'n':
                    break
                elif merge_multiple.lower() == 'y':
                    merger = PdfFileMerger()

                    for file in pdf_files:
                        merger.append(file, 'rb')

                    # p = pathlib.PureWindowsPath(jpg_files[0]).parent
                    merger.write(new_filename_path + "/merged.pdf") # merge the files into one file
                    merger.close()
                    break
            except KeyboardInterrupt:
                print('\n')
                return


if __name__ == '__main__':
    main()
