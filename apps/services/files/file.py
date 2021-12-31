import sys
import os
import traceback
import os
import csv
import sys
import logging
import traceback

from os import listdir
from pathlib import Path
from os.path import isfile, join
from django.conf import settings

logger = logging.getLogger("file_processor")


class FileProcessingTool:
    ACCEPTED_EXTENSIONS = [".csv", ".xls", ".xlsx"]
    DISALLOWED_NAMES = [".", "..", ".DS_Store"]

    @staticmethod
    def archive_file(file_path, filename):
        try:
            archive_dir = settings.ARCHIVE_DIR
            destination_dir = join(archive_dir, filename)
            complete_file_path = join(file_path, filename)
            os.rename(complete_file_path, destination_dir)
        except Exception as err:
            traceback_str = traceback.format_exc()
            print(traceback_str)
            return False
        else:
            return True

    @staticmethod
    def get_unprocessed_files(new_files: list) -> list:
        fn_name = sys._getframe(0).f_code.co_name

        # Fetch files from archive folder
        logger.info("Trying to make a list of archived files.")
        archived_files = listdir(settings.ARCHIVE_DIR)
        logger.info("There are {} archived files.".format(len(archived_files)))

        # Remove already processed files from list of to be processed files
        filename_list = list(set(new_files) - set(archived_files))
        logger.info(
            "There are {} new invoices to be processed.".format(len(filename_list))
        )

        filenames = []
        if filename_list:
            accepted_extensions = FileProcessingTool.ACCEPTED_EXTENSIONS
            filenames = [
                file
                for file in filename_list
                if file not in FileProcessingTool.DISALLOWED_NAMES
            ]
            filenames = [
                file
                for file in filenames
                if FileProcessingTool.get_extension(file) in accepted_extensions
            ]
        logger.info("Finally, I've got a file list: {}.".format(",".join(filenames)))
        return filenames

    @staticmethod
    def is_file_exists(_path):
        _file = Path(_path)
        if not _file.is_file():
            return False
        return True

    @staticmethod
    def remove_file(_path):
        try:
            if FileProcessingTool.is_file_exists(_path):
                os.remove(_path)
        except:
            pass
        else:
            print(f"{_path} removed")

    @staticmethod
    def is_folder_exists(_dir):
        if os.path.exists(_dir) and os.path.isdir(_dir):
            return True
        return False

    @staticmethod
    def get_extension(filename):
        return Path(filename).suffix

    @staticmethod
    def get_file_name(file_path):
        return file_path.split("/")[-1]

    @staticmethod
    def get_number_of_files_in_a_folder(dir):
        all_files = FileProcessingTool.scan_dir(dir)
        return len(all_files)

    @staticmethod
    def scan_dir(_dir):
        if not FileProcessingTool.is_folder_exists(_dir):
            print("File with path %s not found." % _dir)
            return None

        only_files = [f for f in listdir(_dir) if isfile(join(_dir, f))]
        return only_files

    @staticmethod
    def check_and_create_dir(dir_name, retrn_val=False):
        not_exists = not FileProcessingTool.is_folder_exists(dir_name)
        if not_exists:
            os.makedirs(dir_name)
            print("Directory <" + dir_name + "> created")
        else:
            print("Directory <" + dir_name + "> already exists")
        if retrn_val:
            return not_exists

    @staticmethod
    def get_archive_dir(self, ftp_folder=None):
        path = [settings.FILES_DIR, "ARCHIVE"]
        temp_dir = os.path.join(*path)
        FileProcessingTool.check_and_create_dir(temp_dir)
        return temp_dir

    @staticmethod
    def get_file_content(file_content=None):
        if isinstance(file_content, str):
            temp_lines = (
                str(file_content).replace(" ", "_")
                + "b\n"
                + str(file_content).replace(" ", "_")
            )
        else:
            temp_lines = (
                str(file_content.readline()).replace(" ", "_")
                + "b\n"
                + str(file_content.readline()).replace(" ", "_")
            )
        return temp_lines

    @staticmethod
    def get_delimeter(file_path="", file_content=None):
        """
        this helps to find the seperator or delimeter of a csv file

        Parameters
        ----------
        file_path : string
            file name concatenated with file path
        """
        if not file_content:
            with open(file_path, "rb") as csvfile:
                temp_lines = FileProcessingTool.get_file_content(csvfile)

        else:
            temp_lines = FileProcessingTool.get_file_content(file_content)
        dialect = csv.Sniffer().sniff(temp_lines, delimiters=":;,|")
        return dialect.delimiter
