import abc


class FileReader:
    def __init__(self, *args, **kwargs):
        self.file_path = kwargs.get("file_path")
        self.file_name = kwargs.get("file_name")
        self.logger = kwargs.get("logger")

    @abc.abstractmethod
    def read_file(_path):
        pass
