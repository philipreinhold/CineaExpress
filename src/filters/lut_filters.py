import numpy as np
import cv2

class LUTFilter:
    def __init__(self, lut_path):
        self.lut = self._load_lut(lut_path)

    def _load_lut(self, lut_path):
        """Lädt eine 3D-LUT-Datei."""
        lut = cv2.imread(lut_path, cv2.IMREAD_UNCHANGED)
        lut = lut.astype(np.float32) / 255.0
        return lut

    def apply_lut(self, image):
        """Wendet die 3D-LUT auf das Bild an."""
        return cv2.transform(image, self.lut)

class ColorFilter:
    def apply_grayscale(self, image):
        """Wendet einen Graustufen-Filter auf das Bild an."""
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def apply_sepia(self, image):
        """Wendet einen Sepia-Filter auf das Bild an."""
        sepia_filter = np.array([[0.272, 0.534, 0.131],
                                 [0.349, 0.686, 0.168],
                                 [0.393, 0.769, 0.189]])
        return cv2.transform(image, sepia_filter)
