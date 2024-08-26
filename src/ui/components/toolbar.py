from PySide6.QtWidgets import QToolBar, QFileDialog
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Signal

class Toolbar(QToolBar):
    open_image = Signal(str)
    save_image = Signal()
    rotate_image = Signal()
    flip_horizontal = Signal()
    flip_vertical = Signal()
    enable_crop = Signal()
    enable_draw = Signal()
    zoom_in = Signal()
    zoom_out = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_actions()

    def setup_actions(self):
        self.addAction(self.create_action("Open", "open.png", self.open_image_dialog))
        self.addAction(self.create_action("Save", "save.png", self.save_image.emit))
        self.addAction(self.create_action("Rotate", "rotate.png", self.rotate_image.emit))
        self.addAction(self.create_action("Flip H", "flip_h.png", self.flip_horizontal.emit))
        self.addAction(self.create_action("Flip V", "flip_v.png", self.flip_vertical.emit))
        self.addAction(self.create_action("Crop", "crop.png", self.enable_crop.emit))
        self.addAction(self.create_action("Draw", "draw.png", self.enable_draw.emit))
        self.addAction(self.create_action("Zoom In", "zoom_in.png", self.zoom_in.emit))
        self.addAction(self.create_action("Zoom Out", "zoom_out.png", self.zoom_out.emit))

    def create_action(self, text, icon_name, slot):
        action = QAction(QIcon(f"src/resources/icons/{icon_name}"), text, self)
        action.triggered.connect(slot)
        return action

    def open_image_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.open_image.emit(file_name)