from django.test import TestCase
from pages.models import extend_markdown

class MarkdownExtenstionTests(TestCase):
    
    fixtures = ['files.json']
    
    def test_image_number_reference(self):
        markdown_before = "![Caption][5]"
        markdown_after = "![Caption][5]\n[5]: /files/get/5"
        self.assertEquals(markdown_after, extend_markdown(markdown_before))
    
    def test_image_number_existing_reference(self):
        markdown = "![Caption][5]\n[5]: /files/get/5"
        self.assertEquals(markdown, extend_markdown(markdown))
        