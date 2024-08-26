from PySide6.QtGui import QImage, QPixmap
from PIL import Image
import numpy as np

def qimage_to_numpy(qimage: QImage) -> np.ndarray:
    """Convert QImage to numpy array."""
    width = qimage.width()
    height = qimage.height()

    ptr = qimage.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr

def numpy_to_qimage(arr: np.ndarray) -> QImage:
    """Convert numpy array to QImage."""
    height, width, channel = arr.shape
    bytesPerLine = 3 * width
    return QImage(arr.data, width, height, bytesPerLine, QImage.Format_RGB888)

def pil_to_qpixmap(pil_image: Image.Image) -> QPixmap:
    """Convert PIL Image to QPixmap."""
    qimage = pil_to_qimage(pil_image)
    return QPixmap.fromImage(qimage)

def pil_to_qimage(pil_image: Image.Image) -> QImage:
    """Convert PIL Image to QImage."""
    if pil_image.mode == "RGB":
        r, g, b = pil_image.split()
        pil_image = Image.merge("RGB", (b, g, r))
    elif pil_image.mode == "RGBA":
        r, g, b, a = pil_image.split()
        pil_image = Image.merge("RGBA", (b, g, r, a))
    
    im2 = pil_image.convert("RGBA")
    data = im2.tobytes("raw", "RGBA")
    qimage = QImage(data, im2.size[0], im2.size[1], QImage.Format_RGBA8888)
    return qimage

# Weitere Utility-Funktionen...