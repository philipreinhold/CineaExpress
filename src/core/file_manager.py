import os
from PIL import Image

class FileManager:
    def __init__(self):
        pass

    def load_image(self, image_path):
        """Lädt ein Bild von der Festplatte."""
        if os.path.exists(image_path):
            image = Image.open(image_path)
            return image
        else:
            raise FileNotFoundError(f"Datei {image_path} nicht gefunden.")

    def save_image(self, image, output_path):
        """Speichert ein Bild auf der Festplatte."""
        image.save(output_path)

    def get_supported_formats(self):
        """Gibt eine Liste der unterstützten Bildformate zurück."""
        return ["png", "jpg", "jpeg", "bmp", "gif"]
