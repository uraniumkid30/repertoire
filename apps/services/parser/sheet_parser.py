import re
import abc
import traceback
import pandas as pd


class SheetParser(metaclass=abc.ABCMeta):
    def __init__(self, _sheet, **kwargs):
        self.sheet = _sheet
        self.filename = kwargs.get("filename", None)

    def parse_sheet(self):
        result = []
        if self.sheet is None:
            return None
        else:
            try:
                result = self.sheet.to_dict("records")
            except:
                print(f"This stopped me from parsing file: {self.filename}")
                print(traceback.format_exc())
            finally:
                return result
