from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt
from PIL import Image

class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
        self.current_image = None  # Zum Speichern des aktuellen Bildes

    def load_image(self, image_path):
        self.current_image = Image.open(image_path)
        self.display_image(self.current_image)

    def display_image(self, image):
        qimage = self.pil_image_to_qimage(image)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap)

    def rotate_image(self):
        if self.current_image:
            self.current_image = self.current_image.rotate(90, expand=True)
            self.display_image(self.current_image)

    def flip_image_horizontal(self):
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.display_image(self.current_image)

    def flip_image_vertical(self):
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.display_image(self.current_image)

    def pil_image_to_qimage(self, pil_image):
        """Konvertiert ein PIL-Bild in ein QImage."""
        if pil_image.mode in ["RGB", "RGBA"]:
            qimage = QImage(pil_image.tobytes(), pil_image.size[0], pil_image.size[1], QImage.Format_RGB888)
        else:
            pil_image = pil_image.convert("RGBA")
            qimage = QImage(pil_image.tobytes(), pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
        return qimage
