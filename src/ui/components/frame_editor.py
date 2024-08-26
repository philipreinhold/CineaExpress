import logging
from PySide6.QtWidgets import QGraphicsRectItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QRectF, Signal, QObject

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class FrameEditorSignals(QObject):
    frame_moved = Signal()

class FrameEditor(QGraphicsRectItem):
    def __init__(self, rect: QRectF, parent=None):
        super().__init__(rect, parent)
        self.signals = FrameEditorSignals()
        self.frame_moved = self.signals.frame_moved

        self.setFlag(QGraphicsRectItem.ItemIsMovable)
        self.setFlag(QGraphicsRectItem.ItemIsSelectable)
        
        self.frame_color = QColor("red")
        self.frame_pen_width = 2
        self.frame_style = Qt.SolidLine
        
        self.update_pen()
        logger.info("FrameEditor initialized")

    def update_pen(self):
        pen = QPen(self.frame_color, self.frame_pen_width, self.frame_style)
        self.setPen(pen)

    def set_color(self, color: QColor):
        self.frame_color = color
        self.update_pen()
        logger.debug(f"Frame color set to {color.name()}")

    def set_pen_width(self, width: int):
        self.frame_pen_width = width
        self.update_pen()
        logger.debug(f"Frame pen width set to {width}")

    def set_style(self, style: Qt.PenStyle):
        self.frame_style = style
        self.update_pen()
        logger.debug(f"Frame style set to {style}")

    def set_format(self, format_str):
        try:
            width, height = map(float, format_str.split(':'))
            current_rect = self.rect()
            new_height = current_rect.width() * height / width
            new_rect = QRectF(current_rect.x(), current_rect.y(), current_rect.width(), new_height)
            self.setRect(new_rect)
            self.frame_moved.emit()
            logger.debug(f"Frame format set to {format_str}")
        except Exception as e:
            logger.error(f"Error setting frame format: {str(e)}")

    def set_width(self, width_percentage):
        if self.scene():
            try:
                scene_rect = self.scene().sceneRect()
                new_width = scene_rect.width() * width_percentage / 100
                current_rect = self.rect()
                new_height = new_width * current_rect.height() / current_rect.width()
                new_rect = QRectF(current_rect.x(), current_rect.y(), new_width, new_height)
                self.setRect(new_rect)
                self.frame_moved.emit()
                logger.debug(f"Frame width set to {width_percentage}%")
            except Exception as e:
                logger.error(f"Error setting frame width: {str(e)}")
        else:
            logger.warning("FrameEditor is not in a scene")

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.scene():
            self.frame_moved.emit()
            logger.debug("Frame moved")