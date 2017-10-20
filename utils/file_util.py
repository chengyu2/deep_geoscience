import fnmatch
import os
import sys

import shutil

if sys.version_info[0] == 3:
    import pickle
else:
    import cPickle as pickle


import errno


class FileUtil:


    @staticmethod
    def validate_file(file_path):
        """
        Method to ensure that the file and exists at the path
        If it doesn't exist it will create a blank file and
        the necessary folders at the path provided.
        :param file_path: Path to the file to be validated
        :return: None
        """

        if not os.path.isfile(file_path):
            try:
                # Create the directories if they do not alread exist
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
            file = open(file_path, 'w+')
            file.close()

    @staticmethod
    def validate_folder(folder_path):
        """
        Same as validate_file but for folders
        :param folder_path: Path to the folder
        :return: Nonet
        """
        if not os.path.isdir(folder_path):
            try:
                os.makedirs(os.path.abspath(folder_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    @staticmethod
    def is_folder(folder_path):
        return os.path.isdir(folder_path)

    @staticmethod
    def is_file(file_path):
        return os.path.isfile(file_path)


    @staticmethod
    def find_files(base: str, pattern)-> []:
        '''Return list of files matching pattern in base folder.'''
        return [n for n in fnmatch.filter(os.listdir(base), pattern) if
                os.path.isfile(os.path.join(base, n))]

    @staticmethod
    def clear_folder(folder_path):
        """
        Clears all files at specified folder path
        :param folder_path:
        :return: None
        """
        for file_ in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as e:
                print(e)

    @classmethod
    def delete_file(cls, file_path):
        if cls.is_file(file_path=file_path):
            os.remove(path=file_path)

    @staticmethod
    def delete_folder(dir_name):
        shutil.rmtree(path=dir_name)

    @staticmethod
    def dump_object(obj, file_path):
        """
        Dumps an object into the a file at the path provided
        :param obj: Object that needs to be dumped
        :param file_path: Path of target pickle file
        :return:
        """
        FileUtil.validate_file(file_path)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)


    @staticmethod
    def load_object(file_path):

        with open(file_path, "rb") as file:
            obj = pickle.load(file)

        return obj



class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)