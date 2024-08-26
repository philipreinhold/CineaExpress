from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QLineEdit, QTextEdit, QPushButton
from PySide6.QtCore import Signal, Qt

class Sidebar(QWidget):
    frame_format_changed = Signal(str)
    frame_width_changed = Signal(int)
    brightness_changed = Signal(int)
    contrast_changed = Signal(int)
    grayscale_intensity_changed = Signal(int)
    sepia_intensity_changed = Signal(int)
    add_text_requested = Signal(str, str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.setup_frame_format()
        self.setup_frame_width()
        self.setup_image_adjustments()
        self.setup_text_settings()

    def setup_frame_format(self):
        self.layout.addWidget(QLabel("Frame Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["16:9", "4:3", "1:1", "2.35:1", "21:9"])
        self.format_combo.currentTextChanged.connect(self.frame_format_changed.emit)
        self.layout.addWidget(self.format_combo)

    def setup_frame_width(self):
        self.layout.addWidget(QLabel("Frame Width:"))
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(10, 100)
        self.width_slider.setValue(80)
        self.width_slider.valueChanged.connect(self.frame_width_changed.emit)
        self.layout.addWidget(self.width_slider)

    def setup_image_adjustments(self):
        self.add_slider("Brightness", -100, 100, self.brightness_changed)
        self.add_slider("Contrast", -100, 100, self.contrast_changed)
        self.add_slider("Grayscale Intensity", 0, 100, self.grayscale_intensity_changed)
        self.add_slider("Sepia Intensity", 0, 100, self.sepia_intensity_changed)

    def add_slider(self, name, min_val, max_val, signal):
        self.layout.addWidget(QLabel(name))
        slider = QSlider(Qt.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(0)
        slider.valueChanged.connect(signal)
        self.layout.addWidget(slider)

    def setup_text_settings(self):
        self.layout.addWidget(QLabel("Scene Text"))
        self.scene_name_input = QLineEdit()
        self.scene_name_input.setPlaceholderText("Scene Name")
        self.layout.addWidget(self.scene_name_input)

        self.scene_description_input = QTextEdit()
        self.scene_description_input.setPlaceholderText("Scene Description")
        self.layout.addWidget(self.scene_description_input)

        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(['8', '10', '12', '14', '16', '18', '20', '24', '28', '32' , '44' , '56' , '64' , '72' , '86' , '101'])
        self.font_size_combo.setCurrentText('14')
        self.layout.addWidget(self.font_size_combo)

        add_text_button = QPushButton("Add Text to Scene")
        add_text_button.clicked.connect(self.emit_add_text)
        self.layout.addWidget(add_text_button)

    def emit_add_text(self):
        self.add_text_requested.emit(
            self.scene_name_input.text(),
            self.scene_description_input.toPlainText(),
            int(self.font_size_combo.currentText())
        )