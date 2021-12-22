# for adyen
import logging
from .sheet_parser import SheetParser


class ExcelDataParser(SheetParser):
    def __init__(self, _sheet, **kwargs):
        self.sheet = _sheet
