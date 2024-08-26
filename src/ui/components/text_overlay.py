from PySide6.QtWidgets import QGraphicsItemGroup, QGraphicsTextItem
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import QPointF

class TextOverlay(QGraphicsItemGroup):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.name_item = QGraphicsTextItem()
        self.desc_item = QGraphicsTextItem()
        
        self.addToGroup(self.name_item)
        self.addToGroup(self.desc_item)
        
        self.set_font_size(14)
        self.set_color(QColor("white"))

    def set_text(self, name: str, description: str):
        self.name_item.setPlainText(name)
        self.desc_item.setPlainText(description)

    def set_font_size(self, size: int):
        name_font = QFont("Arial", size)
        name_font.setBold(True)
        self.name_item.setFont(name_font)
        
        desc_font = QFont("Arial", size)
        self.desc_item.setFont(desc_font)

    def set_color(self, color: QColor):
        self.name_item.setDefaultTextColor(color)
        self.desc_item.setDefaultTextColor(color)

    def update_position(self, frame_rect):
        self.name_item.setPos(frame_rect.topLeft() + QPointF(10, -self.name_item.font().pointSize() * 2 - 10))
        self.desc_item.setPos(frame_rect.topLeft() + QPointF(10, -self.desc_item.font().pointSize() - 5))