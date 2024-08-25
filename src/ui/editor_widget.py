from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, 
                               QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem, 
                               QColorDialog, QGraphicsItem)
from PySide6.QtGui import QPixmap, QPen, QColor, QFont, QTransform, QPainterPath, QImage, QPainter
from PySide6.QtCore import Qt, QRectF, QPointF, QLineF, QBuffer
from PIL import Image, ImageEnhance, ImageOps
import io

class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.layout.addWidget(self.graphics_view)

        self.pixmap_item = None
        self.frame_item = None
        self.frame_rect = QRectF()
        self.text_items = []
        self.zoom_factor = 1.0
        self.current_image = None

        # Framing-Einstellungen
        self.frame_format = (16, 9)  # Standardmäßig 16:9
        self.frame_color = QColor("red")
        self.frame_pen_width = 2
        self.frame_style = Qt.SolidLine

        # Schieberegler-Werte
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
        self.frame_drag_start = None
        
        # änderung für das aufziehen und kleine rmachen dingens
        self.graphics_view.setResizeAnchor(QGraphicsView.AnchorViewCenter)
        self.graphics_view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.pixmap_item:
            self.fit_in_view()

    def fit_in_view(self):
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.update_frame()    

    def load_image(self, image_path):
        print(f"Attempting to load image: {image_path}")  # Debug-Ausgabe
        try:
            self.current_image = Image.open(image_path)
            self.display_image(self.current_image)
        except Exception as e:
            print(f"Error in load_image: {str(e)}")  # Debug-Ausgabe
            raise

    def display_image(self, image):
        print("Displaying image")  # Debug-Ausgabe
        qimage = self.pil_image_to_qimage(image)
        pixmap = QPixmap.fromImage(qimage)
        if self.pixmap_item:
            self.graphics_scene.removeItem(self.pixmap_item)
        self.pixmap_item = QGraphicsPixmapItem(pixmap)
        self.graphics_scene.addItem(self.pixmap_item)
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self.update_frame()
        print("Image displayed successfully")  # Debug-Ausgabe

    def set_frame_width(self, width_percentage):
        if self.pixmap_item:
            image_rect = self.pixmap_item.boundingRect()
            max_width = min(image_rect.width(), image_rect.height() * self.frame_format[0] / self.frame_format[1])
            width = max_width * (width_percentage / 100)
            frame_height = width * self.frame_format[1] / self.frame_format[0]
            self.frame_rect = QRectF(
                (image_rect.width() - width) / 2,
                (image_rect.height() - frame_height) / 2,
                width, frame_height
            )
            self.update_frame()

    def update_frame(self):
        if self.frame_item:
            self.graphics_scene.removeItem(self.frame_item)
        pen = QPen(self.frame_color, self.frame_pen_width, self.frame_style)
        self.frame_item = self.graphics_scene.addRect(self.frame_rect, pen)
        self.frame_item.setFlag(QGraphicsItem.ItemIsMovable)
        self.frame_item.setFlag(QGraphicsItem.ItemIsSelectable)

    def set_zoom(self, zoom):
        self.zoom_factor = zoom / 100.0
        self.graphics_view.setTransform(QTransform().scale(self.zoom_factor, self.zoom_factor))

    def add_text_to_scene(self, scene_name, scene_description):
        if self.frame_item:
            frame_rect = self.frame_item.rect()
            name_item = QGraphicsTextItem(scene_name)
            name_item.setFont(QFont("Arial", 12, QFont.Bold))
            name_item.setDefaultTextColor(QColor("white"))
            name_item.setPos(frame_rect.topLeft() + QPointF(10, 10))
            
            desc_item = QGraphicsTextItem(scene_description)
            desc_item.setFont(QFont("Arial", 10))
            desc_item.setDefaultTextColor(QColor("white"))
            desc_item.setPos(frame_rect.topLeft() + QPointF(10, 40))
            
            self.graphics_scene.addItem(name_item)
            self.graphics_scene.addItem(desc_item)
            self.text_items.extend([name_item, desc_item])

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
        self.graphics_view.setCursor(Qt.CrossCursor)

    def enable_drawing(self):
        self.drawing = True
        self.cropping = False
        self.graphics_view.setCursor(Qt.CrossCursor)

    def change_pen_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.pen.setColor(color)

    def set_pen_width(self, width):
        self.pen.setWidth(width)

    def mousePressEvent(self, event):
        if self.frame_item and self.frame_item.isUnderMouse():
            self.frame_drag_start = event.pos()
        elif self.drawing:
            self.last_point = self.graphics_view.mapToScene(event.pos())
            self.drawing_item = QGraphicsPathItem()
            self.drawing_item.setPen(self.pen)
            self.graphics_scene.addItem(self.drawing_item)
            path = QPainterPath()
            path.moveTo(self.last_point)
            self.drawing_item.setPath(path)
        elif self.cropping:
            self.crop_start_pos = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.frame_drag_start:
            delta = event.pos() - self.frame_drag_start
            self.frame_rect.translate(delta.x(), delta.y())
            self.update_frame()
            self.frame_drag_start = event.pos()
        elif self.drawing and self.drawing_item:
            new_point = self.graphics_view.mapToScene(event.pos())
            path = self.drawing_item.path()
            path.lineTo(new_point)
            self.drawing_item.setPath(path)
            self.last_point = new_point
        elif self.cropping and self.crop_start_pos:
            rect = QRectF(self.graphics_view.mapToScene(self.crop_start_pos), self.graphics_view.mapToScene(event.pos()))
            if self.current_rect:
                self.graphics_scene.removeItem(self.current_rect)
            self.current_rect = self.graphics_scene.addRect(rect, self.pen)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.frame_drag_start:
            self.frame_drag_start = None
        elif self.drawing:
            self.drawing = False
            self.graphics_view.setCursor(Qt.ArrowCursor)
        elif self.cropping and self.crop_start_pos:
            rect = QRectF(self.graphics_view.mapToScene(self.crop_start_pos), self.graphics_view.mapToScene(event.pos()))
            self.crop_image(rect)
            self.crop_start_pos = None
            self.cropping = False
            self.graphics_view.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

    def crop_image(self, rect):
        if self.current_image:
            rect = rect.toRect()
            x1, y1, x2, y2 = rect.left(), rect.top(), rect.right(), rect.bottom()
            self.current_image = self.current_image.crop((x1, y1, x2, y2))
            self.apply_adjustments()

    def zoom_in(self):
        self.zoom_factor *= 1.25
        self.graphics_view.scale(1.25, 1.25)

    def zoom_out(self):
        self.zoom_factor *= 0.8
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

        if self.brightness_value != 0:
            factor = 1 + (self.brightness_value / 100.0)
            adjusted_image = ImageEnhance.Brightness(adjusted_image).enhance(factor)

        if self.contrast_value != 0:
            factor = 1 + (self.contrast_value / 100.0)
            adjusted_image = ImageEnhance.Contrast(adjusted_image).enhance(factor)

        if self.grayscale_intensity > 0:
            gray_image = ImageOps.grayscale(adjusted_image)
            adjusted_image = Image.blend(adjusted_image.convert("RGB"), gray_image.convert("RGB"), self.grayscale_intensity / 100.0)

        if self.sepia_intensity > 0:
            sepia_image = ImageOps.colorize(adjusted_image.convert("L"), "#704214", "#C0C0C0")
            adjusted_image = Image.blend(adjusted_image.convert("RGB"), sepia_image.convert("RGB"), self.sepia_intensity / 100.0)

        self.display_image(adjusted_image)

    def pil_image_to_qimage(self, pil_image):
        if pil_image.mode == "RGB":
            r, g, b = pil_image.split()
            pil_image = Image.merge("RGB", (b, g, r))
        elif pil_image.mode == "RGBA":
            r, g, b, a = pil_image.split()
            pil_image = Image.merge("RGBA", (b, g, r, a))
        elif pil_image.mode == "L":
            pil_image = pil_image.convert("RGBA")
        
        im2 = pil_image.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qimage = QImage(data, im2.size[0], im2.size[1], QImage.Format_RGBA8888)
        return qimage

    def save_image(self, output_path):
        if self.current_image and self.pixmap_item:
            # Erstelle ein neues Bild mit dem Frame und Text
            scene = self.graphics_scene
            view_rect = self.graphics_view.viewport().rect()
            image = QImage(view_rect.size(), QImage.Format_ARGB32)
            image.fill(Qt.transparent)

            painter = QPainter(image)
            scene.render(painter, QRectF(image.rect()), scene.itemsBoundingRect())
            painter.end()

            # Konvertiere QImage zu PIL Image
            buffer = QBuffer()
            buffer.open(QBuffer.ReadWrite)
            image.save(buffer, "PNG")
            pil_img = Image.open(io.BytesIO(buffer.data()))

            pil_img.save(output_path)
            print(f"Image saved with frame and text to {output_path}")

    def move_frame(self, dx, dy):
        self.frame_rect.translate(dx, dy)
        self.update_frame()