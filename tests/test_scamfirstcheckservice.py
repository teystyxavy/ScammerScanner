import unittest
from unittest.mock import patch
from app.services import ScamFirstCheckService

class TestScamFirstCheckService(unittest.TestCase):
    """
    TEST SCENARIO 1:
    Proper text with no spelling mistakes and no URLs

    TEST SCENARIO 2:
    Proper text with no spelling mistakes and proper URLs (non-malicious)

    TEST SCENARIO 3:
    Text with spelling mistakes and no URLs

    TEST SCENARIO 4:
    Proper text with no spelling mistakes and malicious URLs
    """

    def setUp(self):
        self.service = None

    def test_scenario1(self):
        text = "This is a test sentence with no errors."

        self.service = ScamFirstCheckService(text=text)
        self.assertFalse(self.service.check_spelling())
        self.assertFalse(self.service.check_urls())

    def test_scenario2(self):
        text = "Visit our website at https://example.com for more info."

        self.service = ScamFirstCheckService(text=text)
        self.assertFalse(self.service.check_spelling())
        self.assertFalse(self.service.check_urls())

    def test_scenario3(self):
        text = "This sentnce has a speling eror."

        self.service = ScamFirstCheckService(text=text)
        self.assertTrue(self.service.check_spelling())
        self.assertFalse(self.service.check_urls())

    @patch.object(ScamFirstCheckService, 'check_urls', return_value=True)
    def test_scenario4(self, mock_is_malicious):
        text = "Click here: http://malicious.com to win a prize!"

        self.service = ScamFirstCheckService(text=text)
        self.assertFalse(self.service.check_spelling())
        self.assertTrue(self.service.check_urls())

if __name__ == '__main__':
    unittest.main()
