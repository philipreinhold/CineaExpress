import logging
import weakref
from PySide6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFileDialog
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QRectF
from src.services.image_processing_service import ImageProcessingService
from src.ui.components.frame_editor import FrameEditor
from src.ui.components.text_overlay import TextOverlay

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EditorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.layout.addWidget(self.graphics_view)

        self.pixmap_item = None
        self._frame_editor = None
        self.text_overlay = TextOverlay()
        self.graphics_scene.addItem(self.text_overlay)

        self.image_service = ImageProcessingService()

    @property
    def frame_editor(self):
        return self._frame_editor() if self._frame_editor is not None else None

    @frame_editor.setter
    def frame_editor(self, value):
        self._frame_editor = weakref.ref(value) if value is not None else None

    def load_image(self, image_path):
        try:
            image = self.image_service.load_image(image_path)
            self.display_image(image, init_frame=True)
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")

    def save_image(self):
        if not self.pixmap_item:
            logger.warning("No image to save")
            return
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            try:
                self.image_service.save_image(self.pixmap_item.pixmap().toImage(), file_path)
                logger.info(f"Image saved to {file_path}")
            except Exception as e:
                logger.error(f"Error saving image: {str(e)}")

    def display_image(self, image, init_frame=False):
        if isinstance(image, QImage):
            pixmap = QPixmap.fromImage(image)
        else:
            pixmap = QPixmap(image)
        
        if self.pixmap_item:
            self.graphics_scene.removeItem(self.pixmap_item)
        self.pixmap_item = self.graphics_scene.addPixmap(pixmap)
        self.graphics_view.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        
        if init_frame or not self.is_frame_editor_valid():
            self.init_frame_editor()
        else:
            self.update_frame_editor_on_image_change()
        
        self.update_text_overlay()

    def init_frame_editor(self):
        if self.frame_editor:
            self.graphics_scene.removeItem(self.frame_editor)
        if self.pixmap_item:
            image_rect = self.pixmap_item.boundingRect()
            frame_rect = QRectF(image_rect.width() * 0.1, image_rect.height() * 0.1,
                                image_rect.width() * 0.8, image_rect.height() * 0.8)
            new_frame_editor = FrameEditor(frame_rect)
            self.graphics_scene.addItem(new_frame_editor)
            new_frame_editor.setParentItem(self.pixmap_item)
            self.frame_editor = new_frame_editor
            logger.info("Frame editor initialized")

    def update_frame_editor_on_image_change(self):
        if self.is_frame_editor_valid() and self.pixmap_item:
            image_rect = self.pixmap_item.boundingRect()
            frame_rect = self.frame_editor.rect()
            new_rect = QRectF(
                frame_rect.x() * image_rect.width() / self.frame_editor.parentItem().boundingRect().width(),
                frame_rect.y() * image_rect.height() / self.frame_editor.parentItem().boundingRect().height(),
                frame_rect.width() * image_rect.width() / self.frame_editor.parentItem().boundingRect().width(),
                frame_rect.height() * image_rect.height() / self.frame_editor.parentItem().boundingRect().height()
            )
            self.frame_editor.setRect(new_rect)
            self.frame_editor.setParentItem(self.pixmap_item)
            logger.info("Frame editor updated on image change")

    def is_frame_editor_valid(self):
        return self.frame_editor is not None and self.frame_editor.scene() is not None

    def ensure_frame_editor(self):
        if not self.is_frame_editor_valid():
            logger.warning("Frame editor is not valid, reinitializing...")
            self.init_frame_editor()

    def update_text_overlay(self):
        if self.is_frame_editor_valid():
            self.text_overlay.update_position(self.frame_editor.rect())

    def set_frame_format(self, format_str):
        self.ensure_frame_editor()
        if self.is_frame_editor_valid():
            self.frame_editor.set_format(format_str)
            self.update_text_overlay()
            logger.debug(f"Frame format set to {format_str}")

    def set_frame_width(self, width):
        self.ensure_frame_editor()
        if self.is_frame_editor_valid():
            self.frame_editor.set_width(width)
            self.update_text_overlay()
            logger.debug(f"Frame width set to {width}")

    def rotate_image(self):
        if self.pixmap_item:
            try:
                rotated = self.image_service.rotate_image(self.pixmap_item.pixmap().toImage())
                self.display_image(rotated, init_frame=False)
                logger.info("Image rotated")
            except Exception as e:
                logger.error(f"Error rotating image: {str(e)}")

    def flip_image_horizontal(self):
        if self.pixmap_item:
            try:
                flipped = self.image_service.flip_image_horizontal(self.pixmap_item.pixmap().toImage())
                self.display_image(flipped, init_frame=False)
                logger.info("Image flipped horizontally")
            except Exception as e:
                logger.error(f"Error flipping image horizontally: {str(e)}")

    def flip_image_vertical(self):
        if self.pixmap_item:
            try:
                flipped = self.image_service.flip_image_vertical(self.pixmap_item.pixmap().toImage())
                self.display_image(flipped, init_frame=False)
                logger.info("Image flipped vertically")
            except Exception as e:
                logger.error(f"Error flipping image vertically: {str(e)}")

    def enable_crop(self):
        logger.info("Crop functionality not yet implemented")
        pass

    def enable_drawing(self):
        logger.info("Drawing functionality not yet implemented")
        pass

    def zoom_in(self):
        self.graphics_view.scale(1.2, 1.2)
        logger.debug("Zoomed in")

    def zoom_out(self):
        self.graphics_view.scale(1/1.2, 1/1.2)
        logger.debug("Zoomed out")

    def adjust_brightness(self, value):
        if self.pixmap_item:
            try:
                adjusted = self.image_service.adjust_brightness(self.pixmap_item.pixmap().toImage(), value)
                self.display_image(adjusted, init_frame=False)
                logger.debug(f"Brightness adjusted to {value}")
            except Exception as e:
                logger.error(f"Error adjusting brightness: {str(e)}")

    def adjust_contrast(self, value):
        if self.pixmap_item:
            try:
                adjusted = self.image_service.adjust_contrast(self.pixmap_item.pixmap().toImage(), value)
                self.display_image(adjusted, init_frame=False)
                logger.debug(f"Contrast adjusted to {value}")
            except Exception as e:
                logger.error(f"Error adjusting contrast: {str(e)}")

    def adjust_grayscale_intensity(self, value):
        if self.pixmap_item:
            try:
                adjusted = self.image_service.apply_grayscale(self.pixmap_item.pixmap().toImage(), value)
                self.display_image(adjusted, init_frame=False)
                logger.debug(f"Grayscale intensity adjusted to {value}")
            except Exception as e:
                logger.error(f"Error adjusting grayscale intensity: {str(e)}")

    def adjust_sepia_intensity(self, value):
        if self.pixmap_item:
            try:
                adjusted = self.image_service.apply_sepia(self.pixmap_item.pixmap().toImage(), value)
                self.display_image(adjusted, init_frame=False)
                logger.debug(f"Sepia intensity adjusted to {value}")
            except Exception as e:
                logger.error(f"Error adjusting sepia intensity: {str(e)}")

    def add_text_to_scene(self, name, description, font_size):
        self.ensure_frame_editor()
        if self.is_frame_editor_valid():
            self.text_overlay.set_text(name, description)
            self.text_overlay.set_font_size(font_size)
            self.text_overlay.update_position(self.frame_editor.rect())
            logger.info("Text added to scene")
        else:
            logger.warning("Cannot add text: Frame editor is not valid")