from src.core.image_processor import ImageProcessor
from src.core.file_manager import FileManager

class BatchProcessor:
    def __init__(self, image_paths):
        self.image_paths = image_paths
        self.file_manager = FileManager()

    def process_images(self, output_directory, operation, *args):
        """Führt eine angegebene Operation auf alle Bilder aus."""
        for image_path in self.image_paths:
            image = self.file_manager.load_image(image_path)
            processor = ImageProcessor(image_path)
            processed_image = operation(processor, *args)
            output_path = self._generate_output_path(image_path, output_directory)
            self.file_manager.save_image(processed_image, output_path)

    def _generate_output_path(self, image_path, output_directory):
        """Generiert den Ausgabepfad für ein Bild."""
        base_name = os.path.basename(image_path)
        return os.path.join(output_directory, base_name)
