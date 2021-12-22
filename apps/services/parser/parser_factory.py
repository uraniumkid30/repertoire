from ..files.csv_file_reader import CSVFileReader
from ..files.excel_file_reader import ExcelFileReader


class ParserFactory:
    @staticmethod
    def factory(fileReader, sheet, **kwargs):
        if not fileReader:
            return None

        if isinstance(fileReader, CSVFileReader):
            from .csv_fortnox_parser import CSVParser

            return CSVParser(sheet, **kwargs)
        elif isinstance(fileReader, ExcelFileReader):
            from .excel_data_parser import ExcelDataParser

            return ExcelDataParser(sheet, **kwargs)
        return None
