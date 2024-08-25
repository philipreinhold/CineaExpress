import unittest
from src.core.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ImageProcessor("test_image.jpg")

    def test_rotate(self):
        rotated_image = self.processor.rotate(90)
        self.assertIsNotNone(rotated_image)

    def test_flip_horizontal(self):
        flipped_image = self.processor.flip_horizontal()
        self.assertIsNotNone(flipped_image)

if __name__ == '__main__':
    unittest.main()
