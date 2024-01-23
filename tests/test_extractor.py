import unittest
from extractor import extract_data

class TestExtractor(unittest.TestCase):

    def test_valid_url(self):
        url = 'https://codewithnazam.com/mastering-css-media-queries-for-aevices-a-comprehensive-guide-to-responsive-design/'  # Replace with a valid URL
        result = extract_data(url)
        self.assertIsNotNone(result)
        self.assertIn('title', result)
        self.assertIn('image', result)
        # Add more assertions here

    
    def test_invalid_url(self):
        url = 'http://nonexistentdomain.com'  # Use a clearly invalid URL
        result = extract_data(url)
        # Update this to check for an appropriate error response
        self.assertIn("error", result)

    def test_missing_data(self):
        url = 'https://codewithnazam.com/mastering-css-media-queries-for-aevices-a-comprehensive-guide-to-responsive-design/'  # URL where title is missing
        result = extract_data(url)
        self.assertEqual(result['title'], 'Title not found')

    # Add more test cases...

if __name__ == '__main__':
    unittest.main()

