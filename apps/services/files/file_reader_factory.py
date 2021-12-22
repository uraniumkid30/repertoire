from .file import FileProcessingTool
from .csv_file_reader import CSVFileReader
from .excel_file_reader import ExcelFileReader


class FileReaderFactory:
    @staticmethod
    def factory(file_path, logger=None):
        file_name = FileProcessingTool.get_file_name(file_path)
        file_extension = FileProcessingTool.get_extension(file_name)

        kwargs = {
            "file_path": file_path,
            "file_name": file_name,
            "logger": logger,
        }

        if file_extension == ".csv":
            return CSVFileReader(**kwargs)
        elif file_extension == ".xls" or file_extension == ".xlsx":
            return ExcelFileReader(**kwargs)
        return None
