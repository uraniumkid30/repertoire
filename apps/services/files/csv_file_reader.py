import os
import re
import csv
import logging
import traceback
import pandas as pd
from datetime import datetime

from .file import FileProcessingTool
from .file_reader import FileReader


class CSVFileReader(FileReader):
    def read_file(self, use_pandas=True):
        full_path = self.file_path
        self.delimeter = FileProcessingTool.get_delimeter(full_path)
        if use_pandas:
            sheet = self.pandas_method()
        else:
            sheet = self.natural_method()
        return sheet

    def natural_method(self, filename):
        full_path = self.file_path
        result = None
        try:
            with open(full_path) as f:
                data = csv.reader(f, delimiter=self.delimeter)
                result = [row for row in data]
            return result
        except Exception as err:
            self.logger.error(str(err))
            self.logger.error(traceback.format_exc())
        finally:
            return result

    def pandas_method(
        self,
    ):
        try:
            df_src = pd.DataFrame({})
            types_dict = {}
            extra_options = {}
            if types_dict:
                extra_options.update(
                    {
                        "dtype": types_dict,
                    }
                )
            try:
                df_src = pd.read_csv(
                    open(self.file_path, "r", encoding="utf8", errors="ignore"),
                    sep=self.delimeter,
                )
            except Exception as e:
                self.logger.error(traceback.format_exc())
                df_src = pd.read_csv(
                    self.file_path, sep=self.delimeter, **extra_options
                )

        except:
            self.logger.error(traceback.format_exc())
        finally:
            return df_src
