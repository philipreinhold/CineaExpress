import unittest
from src.core.file_manager import FileManager

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.manager = FileManager()

    def test_load_image(self):
        image = self.manager.load_image("test_image.jpg")
        self.assertIsNotNone(image)

    def test_save_image(self):
        image = self.manager.load_image("test_image.jpg")
        self.manager.save_image(image, "output_image.jpg")
        self.assertTrue(os.path.exists("output_image.jpg"))

if __name__ == '__main__':
    unittest.main()
