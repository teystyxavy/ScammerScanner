import unittest
from PIL import Image
from app.services import ParseTextService

class TestParseTextService(unittest.TestCase):
    def setUp(self):
        self.parser = ParseTextService()
        self.test_image_path = 'tests/tests_image.png'

    def test_load_image(self):
        """
        Tests load_image function from ParseTextService
        """

        image = self.parser.load_image(self.test_image_path)
        self.assertIsInstance(image, Image.Image, "The loaded object is not a PIL Image")

    def test_extract_text(self):
        """
        Tests extract_text function from ParseTextService (runs load_image beforehand)
        """
        image = self.parser.load_image(self.test_image_path)
        text = self.parser.extract_text(image)
        self.assertIsInstance(text, str, "The extracted text is not a string")
        self.assertGreater(len(text), 0, "The extracted text is empty")

if __name__ == '__main__':
    unittest.main()