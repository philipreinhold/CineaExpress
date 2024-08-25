import cv2
import numpy as np

class ImageUtils:
    @staticmethod
    def resize_image(image, width=None, height=None):
        """Ändert die Größe des Bildes auf die angegebene Breite und Höhe."""
        return cv2.resize(image, (width, height))

    @staticmethod
    def add_frame(image, frame_thickness=5, color=(0, 0, 0)):
        """Fügt einen Rahmen um das Bild hinzu."""
        return cv2.copyMakeBorder(image, frame_thickness, frame_thickness, frame_thickness, frame_thickness,
                                  cv2.BORDER_CONSTANT, value=color)

    @staticmethod
    def apply_vignette(image, strength=1.0):
        """Wendet einen Vignetteneffekt auf das Bild an."""
        rows, cols = image.shape[:2]
        kernel_x = cv2.getGaussianKernel(cols, cols / strength)
        kernel_y = cv2.getGaussianKernel(rows, rows / strength)
        kernel = kernel_y * kernel_x.T
        mask = 255 * kernel / np.linalg.norm(kernel)
        vignette = np.copy(image)
        for i in range(3):
            vignette[:, :, i] = vignette[:, :, i] * mask
        return vignette
