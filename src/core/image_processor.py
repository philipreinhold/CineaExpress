from PIL import Image

class ImageProcessor:
    def __init__(self, image_path):
        self.image = Image.open(image_path)

    def crop(self, box):
        """Zuschneiden des Bildes auf die angegebene Box (left, upper, right, lower)."""
        cropped_image = self.image.crop(box)
        return cropped_image

    def rotate(self, angle):
        """Drehen des Bildes um den angegebenen Winkel."""
        rotated_image = self.image.rotate(angle, expand=True)
        return rotated_image

    def flip_horizontal(self):
        """Spiegeln des Bildes entlang der horizontalen Achse."""
        flipped_image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        return flipped_image

    def flip_vertical(self):
        """Spiegeln des Bildes entlang der vertikalen Achse."""
        flipped_image = self.image.transpose(Image.FLIP_TOP_BOTTOM)
        return flipped_image

    def save_image(self, output_path, image=None):
        """Speichern des Bildes im angegebenen Pfad."""
        if image is None:
            image = self.image
        image.save(output_path)
