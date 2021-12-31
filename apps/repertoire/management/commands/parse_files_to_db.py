from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# from apps.user.models import UserProfile
import os
import json
import traceback
from datetime import datetime, timedelta
from apps.repertoire.models import Files, Works
from apps.services.parser.parser_factory import ParserFactory
from apps.services.files.file_reader_factory import FileReaderFactory
from apps.services.files.file import FileProcessingTool


class Command(BaseCommand):
    """Install the theme"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            new_files_dir = settings.NEWFILES_DIR
            new_files = FileProcessingTool.scan_dir(new_files_dir)
            print(new_files)
            unprocessed_files = FileProcessingTool.get_unprocessed_files(new_files)
            all_parsed_file = []
            for n, file_name in enumerate(unprocessed_files, start=1):
                try:
                    file_path = os.path.join(new_files_dir, file_name)
                    print(f"file no {n}:{file_name}.")
                    filefactory_details = {
                        "file_path": file_path,
                    }

                    fileReader = FileReaderFactory.factory(**filefactory_details)
                    sheet = fileReader.read_file(file_path)

                    if sheet is None and not len(sheet):
                        msg_err = (
                            f"Empty file or no values obtained for file {file_name}"
                        )
                        print(msg_err)
                        continue
                    parser = ParserFactory.factory(
                        fileReader,
                        sheet,
                        file_path=file_path,
                    )
                    parsed_sheet = parser.parse_sheet()
                    all_parsed_file.append(
                        {
                            "file_name": file_name,
                            "work_count": len(parsed_sheet),
                            "parsed_sheet": parsed_sheet,
                        }
                    )
                except:
                    pass  # title contributors iswc source  proprietary_id
                finally:
                    FileProcessingTool.archive_file(new_files_dir, file_name)
            else:
                for parsed_file_info in all_parsed_file:
                    files_in_db = Files.objects.filter(
                        file_name=parsed_file_info["file_name"]
                    )
                    if not files_in_db.exists():
                        files_in_db = Files.objects.create(
                            file_name=parsed_file_info["file_name"],
                            work_count=parsed_file_info["work_count"],
                        )
                    else:
                        files_in_db = files_in_db.first()
                    for parsed_file in parsed_file_info["parsed_sheet"]:
                        filter_data = parsed_file.copy()
                        filter_data.update({"music_file": files_in_db})
                        works = Works.objects.filter(**filter_data)
                        if not works.exists():
                            Works.objects.create(**filter_data)

        except Exception as e:
            print(traceback.print_exc())
        finally:
            print(f"Done running app Migrator")
