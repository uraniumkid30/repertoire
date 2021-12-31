from io import StringIO
from django.conf import settings
from django.urls import reverse
from .models import Files, Works
from rest_framework import status
from django.core.management import call_command
from .serializers import FileSerializer, WorkSerializer
from apps.services.files.file import FileProcessingTool
from django.test import TestCase, Client


class RepertoireTest(TestCase):
    def setUp(self) -> None:
        self.processor = FileProcessingTool
        self.client = Client()
        self.test_file = Files.objects.create(file_name="test.csv", work_count=900)
        self.test_work = Works.objects.create(
            music_file=self.test_file,
            proprietary_id=1,
            iswc="west coast",
            source="amazon",
            title="Whale and whales",
            contributors="Obispo Pascal Michel|Florence Lionel Jacques",
        )

    def call_command(self, command_title, *args, **kwargs):
        call_command(
            command_title, *args, stdout=StringIO(), stderr=StringIO(), **kwargs
        )

    def test_parser_management_command(self):
        command_title = "parse_files_to_db"
        self.call_command(command_title)
        new_files_dir = settings.NEWFILES_DIR
        number_of_files_left = self.processor.get_number_of_files_in_a_folder(
            new_files_dir
        )
        self.assertEqual(number_of_files_left, 0)

    def test_get_all_files(self):
        all_files = Files.objects.all()
        response = self.client.get(reverse("api:files-list"))
        serialized_all_files = FileSerializer(all_files, many=True)
        self.assertEqual(response.data, serialized_all_files.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_file(self):

        response = self.client.get(
            reverse("api:files-detail", kwargs={"pk": self.test_file.pk})
        )
        serialized_single_file = FileSerializer(self.test_file)
        self.assertEqual(response.data, serialized_single_file.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_file(self):
        response = self.client.get(reverse("api:files-detail", kwargs={"pk": 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_works_connected_to_a_single_file(self):

        response = self.client.get(
            reverse(
                "api:works-list",
                kwargs={"files_pk": self.test_file.pk},
            )
        )
        works = Works.objects.filter(music_file=self.test_file)
        serialized_single_file = WorkSerializer(works, many=True)
        self.assertEqual(response.data, serialized_single_file.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
