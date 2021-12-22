import xlrd

from .file_reader import FileReader
from .file import FileProcessingTool


class ExcelFileReader(FileReader):
    def read_file(self, _path):
        if not FileProcessingTool.is_file_exists(_path):
            return None

        try:
            sheet_list = []
            work_book = xlrd.open_workbook(_path)
            date_mode = work_book.datemode
            sheet = work_book.sheet_by_index(0)
            first_cell = sheet.cell(0, 0).value

            num_cols = sheet.ncols
            for row_idx in range(0, sheet.nrows):
                cols_list = []
                for col_idx in range(0, num_cols):
                    cell_obj = sheet.cell(row_idx, col_idx)
                    cols_list.append(cell_obj.value)

                sheet_list.append(cols_list)

            return sheet_list
        except Exception as e:
            print(str(e))
            return None
