from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QColorDialog, QGraphicsRectItem
from PySide6.QtGui import QPixmap, QImage, QPen, QColor
from PySide6.QtCore import Qt, QRectF
from PIL import Image, ImageEnhance, ImageOps

class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.setAcceptDrops(True)

        # QGraphicsView und QGraphicsScene
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.layout.addWidget(self.graphics_view)

        self.current_image = None
        self.pixmap_item = None
        self.scale_factor = 1.0

        # Framing-Einstellungen
        self.frame_item = None
        self.frame_format = (16, 9)  # Standardmäßig 16:9
        self.frame_color = QColor("red")
        self.frame_pen_width = 2
        self.frame_style = Qt.SolidLine

        # Schieberegler-Werte speichern
        self.brightness_value = 0
        self.contrast_value = 0
        self.grayscale_intensity = 0
        self.sepia_intensity = 0

        # Zuschnitt- und Zeichenmodus
        self.cropping = False
        self.drawing = False
        self.crop_start_pos = None
        self.current_rect = None
        self.path_item = None
        self.pen = QPen(QColor("red"), 3, Qt.SolidLine)

    def load_image(self, image_path):
        self.current_image = Image.open(image_path)
        self.display_image(self.current_image)

    def save_image(self, output_path):
        if self.current_image:
            self.current_image.save(output_path)

    def display_image(self, image):
        qimage = self.pil_image_to_qimage(image)
        pixmap = QPixmap.fromImage(qimage)
        if self.pixmap_item:
            self.graphics_scene.removeItem(self.pixmap_item)

        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.graphics_scene.addItem(self.pixmap_item)
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

        self.update_frame()

    def update_frame(self):
        if self.frame_item:
            self.graphics_scene.removeItem(self.frame_item)

        image_rect = self.pixmap_item.boundingRect()
        width_ratio = self.frame_format[0] / self.frame_format[1]
        if image_rect.width() / image_rect.height() > width_ratio:
            frame_height = image_rect.height() * 0.9
            frame_width = frame_height * width_ratio
        else:
            frame_width = image_rect.width() * 0.9
            frame_height = frame_width / width_ratio

        frame_rect = QRectF(
            (image_rect.width() - frame_width) / 2,
            (image_rect.height() - frame_height) / 2,
            frame_width, frame_height
        )

        pen = QPen(self.frame_color, self.frame_pen_width, self.frame_style)
        self.frame_item = self.graphics_scene.addRect(frame_rect, pen)

    def set_frame_format(self, format_str):
        width, height = map(float, format_str.split(':'))
        self.frame_format = (width, height)
        self.update_frame()

    def set_frame_pen_width(self, width):
        self.frame_pen_width = width
        self.update_frame()

    def set_frame_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.frame_color = color
        self.update_frame()

    def set_frame_style(self, style):
        self.frame_style = style
        self.update_frame()

    def rotate_image(self):
        if self.current_image:
            self.current_image = self.current_image.rotate(90, expand=True)
            self.apply_adjustments()

    def flip_image_horizontal(self):
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.apply_adjustments()

    def flip_image_vertical(self):
        if self.current_image:
            self.current_image = self.current_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.apply_adjustments()

    def enable_crop(self):
        self.cropping = True
        self.drawing = False
        self.graphics_view.setCursor(Qt.CrossCursor)  # Kreuzcursor für das Zuschneiden

    def enable_drawing(self):
        self.drawing = True
        self.cropping = False
        self.graphics_view.setCursor(Qt.CrossCursor)  # Stift- oder Fadenkreuz-Cursor für das Zeichnen

    def disable_modes(self):
        self.drawing = False
        self.cropping = False
        self.graphics_view.setCursor(Qt.ArrowCursor)  # Zurück zum normalen Cursor

    def change_pen_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen.setColor(color)

    def set_pen_width(self, width):
        self.pen.setWidth(width)

    def mousePressEvent(self, event):
        if self.cropping or self.drawing:
            self.crop_start_pos = event.pos()
            if self.drawing:
                self.path_item = QGraphicsPathItem()
                self.path_item.setPen(self.pen)
                self.graphics_scene.addItem(self.path_item)
                self.path = QPainterPath(self.graphics_view.mapToScene(self.crop_start_pos))

    def mouseMoveEvent(self, event):
        if self.cropping and self.crop_start_pos:
            rect = QRectF(self.graphics_view.mapToScene(self.crop_start_pos), self.graphics_view.mapToScene(event.pos()))
            if self.current_rect:
                self.graphics_scene.removeItem(self.current_rect)
            self.current_rect = self.graphics_scene.addRect(rect, self.pen)
        elif self.drawing and self.crop_start_pos:
            if self.path_item:
                line = QLineF(self.path.currentPosition(), self.graphics_view.mapToScene(event.pos()))
                self.path.lineTo(line.p2())
                self.path_item.setPath(self.path)

    def mouseReleaseEvent(self, event):
        if self.cropping and self.crop_start_pos:
            rect = QRectF(self.graphics_view.mapToScene(self.crop_start_pos), self.graphics_view.mapToScene(event.pos()))
            self.crop_image(rect)
            self.crop_start_pos = None
            self.cropping = False
            self.disable_modes()
        elif self.drawing:
            self.crop_start_pos = None
            self.drawing = False
            self.disable_modes()

    def crop_image(self, rect):
        if self.current_image:
            rect = rect.toRect()
            x1 = int(rect.left())
            y1 = int(rect.top())
            x2 = int(rect.right())
            y2 = int(rect.bottom())
            self.current_image = self.current_image.crop((x1, y1, x2, y2))
            self.apply_adjustments()

    def zoom_in(self):
        self.scale_factor *= 1.25
        self.graphics_view.scale(1.25, 1.25)

    def zoom_out(self):
        self.scale_factor *= 0.8
        self.graphics_view.scale(0.8, 0.8)

    def adjust_brightness(self, value):
        self.brightness_value = value
        self.apply_adjustments()

    def adjust_contrast(self, value):
        self.contrast_value = value
        self.apply_adjustments()

    def adjust_grayscale_intensity(self, value):
        self.grayscale_intensity = value
        self.apply_adjustments()

    def adjust_sepia_intensity(self, value):
        self.sepia_intensity = value
        self.apply_adjustments()

    def apply_adjustments(self):
        if not self.current_image:
            return

        adjusted_image = self.current_image

        # Helligkeit anpassen
        if self.brightness_value != 0:
            enhancer = ImageEnhance.Brightness(adjusted_image)
            factor = 1 + (self.brightness_value / 100.0)
            adjusted_image = enhancer.enhance(factor)

        # Kontrast anpassen
        if self.contrast_value != 0:
            enhancer = ImageEnhance.Contrast(adjusted_image)
            factor = 1 + (self.contrast_value / 100.0)
            adjusted_image = enhancer.enhance(factor)

        # Graustufen anwenden
        if self.grayscale_intensity > 0:
            gray_image = ImageOps.grayscale(adjusted_image)
            adjusted_image = Image.blend(adjusted_image.convert("RGB"), gray_image.convert("RGB"), self.grayscale_intensity / 100.0)

        # Sepia anwenden
        if self.sepia_intensity > 0:
            sepia_image = ImageOps.colorize(adjusted_image.convert("L"), "#704214", "#C0C0C0")
            adjusted_image = Image.blend(adjusted_image.convert("RGB"), sepia_image.convert("RGB"), self.sepia_intensity / 100.0)

        self.display_image(adjusted_image)

    def pil_image_to_qimage(self, pil_image):
        if pil_image.mode in ["RGB", "RGBA"]:
            qimage = QImage(pil_image.tobytes(), pil_image.size[0], pil_image.size[1], QImage.Format_RGB888)
        else:
            pil_image = pil_image.convert("RGBA")
            qimage = QImage(pil_image.tobytes(), pil_image.size[0], pil_image.size[1], QImage.Format_RGBA8888)
        return qimage
