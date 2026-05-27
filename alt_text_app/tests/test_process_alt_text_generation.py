"""
Tests for the background alt-text generation script.
"""

from django.test import TestCase

from alt_text_app.models import GeneratedAltText, ImageDocument
from scripts import process_alt_text_generation


class ProcessAltTextGenerationTest(TestCase):
    """
    Checks background alt-text generation helpers.
    """

    def test_find_pending_alt_text_uses_generated_alt_text_relation(self) -> None:
        """
        Checks that pending documents are found through the generated_alt_text relation.
        """
        doc_without_alt_text = ImageDocument.objects.create(
            original_filename='without.png',
            file_checksum='checksum_without',
            file_size=1024,
            mime_type='image/png',
            file_extension='png',
            processing_status='pending',
        )
        doc_with_pending_alt_text = ImageDocument.objects.create(
            original_filename='pending.png',
            file_checksum='checksum_pending',
            file_size=1024,
            mime_type='image/png',
            file_extension='png',
            processing_status='processing',
        )
        doc_with_completed_alt_text = ImageDocument.objects.create(
            original_filename='completed.png',
            file_checksum='checksum_completed',
            file_size=1024,
            mime_type='image/png',
            file_extension='png',
            processing_status='completed',
        )
        GeneratedAltText.objects.create(
            image_document=doc_with_pending_alt_text,
            status='pending',
        )
        GeneratedAltText.objects.create(
            image_document=doc_with_completed_alt_text,
            status='completed',
        )

        docs = process_alt_text_generation.find_pending_alt_text(batch_size=10)

        self.assertEqual([doc_without_alt_text, doc_with_pending_alt_text], docs)
