import pandas as pd
from .sheet_parser import SheetParser


class CSVParser(SheetParser):
    def parse_sheet(self):
        if isinstance(self.sheet, pd.DataFrame):
            parsed_sheet = super(CSVParser, self).parse_sheet()
            return parsed_sheet
        else:
            return self.sheet
