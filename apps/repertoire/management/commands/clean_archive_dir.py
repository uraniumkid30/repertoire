import os
import traceback
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from apps.services.files.file import FileProcessingTool


class Command(BaseCommand):
    """Clean media files and directory"""

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            archive_directory = FileProcessingTool.get_archive_dir()
            archive_files = FileProcessingTool.scan_dir(archive_directory)
            for file_name in archive_files:
                file_path = os.path.join(archive_directory, file_name)
                FileProcessingTool.remove_file(file_path)
        except Exception as e:
            print(traceback.print_exc())
