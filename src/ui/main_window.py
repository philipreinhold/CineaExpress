from PySide6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QSlider, QComboBox, QLineEdit, QTextEdit, QPushButton
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, Signal
from src.ui.components.editor_widget import EditorWidget
from src.ui.components.toolbar import Toolbar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CineaExpress")
        self.setGeometry(100, 100, 1200, 800)

        # Hauptlayout
        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Editor Widget
        self.editor_widget = EditorWidget(self)
        main_layout.addWidget(self.editor_widget, stretch=3)

        # Rechte Seitenleiste
        sidebar = QWidget()
        sidebar_layout = QVBoxLayout(sidebar)
        
        self.setup_frame_settings(sidebar_layout)
        self.setup_image_adjustments(sidebar_layout)
        self.setup_text_settings(sidebar_layout)

        main_layout.addWidget(sidebar)

        # Toolbar
        self.toolbar = Toolbar(self)
        self.addToolBar(self.toolbar)

        # Verbindungen zwischen Komponenten herstellen
        self.setup_connections()

    def setup_frame_settings(self, layout):
        layout.addWidget(QLabel("Frame Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["16:9", "4:3", "1:1", "2.35:1", "21:9"])
        layout.addWidget(self.format_combo)

        layout.addWidget(QLabel("Frame Width:"))
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(10, 100)
        self.width_slider.setValue(80)
        layout.addWidget(self.width_slider)

    def setup_image_adjustments(self, layout):
        adjustments = [
            ("Brightness", -100, 100),
            ("Contrast", -100, 100),
            ("Grayscale Intensity", 0, 100),
            ("Sepia Intensity", 0, 100)
        ]
        
        for name, min_val, max_val in adjustments:
            layout.addWidget(QLabel(name))
            slider = QSlider(Qt.Horizontal)
            slider.setRange(min_val, max_val)
            slider.setValue(0)
            setattr(self, f"{name.lower().replace(' ', '_')}_slider", slider)
            layout.addWidget(slider)

    def setup_text_settings(self, layout):
        layout.addWidget(QLabel("Scene Text"))
        self.scene_name_input = QLineEdit()
        self.scene_name_input.setPlaceholderText("Scene Number/Name")
        layout.addWidget(self.scene_name_input)

        self.scene_description_input = QTextEdit()
        self.scene_description_input.setPlaceholderText("Shot Description")
        layout.addWidget(self.scene_description_input)

        self.font_size_combo = QComboBox()
        self.font_size_combo.addItems(['8', '10', '12', '14', '16', '18', '20', '24', '28', '32' , '44' , '56' , '64' , '72' , '86' , '101'])
        self.font_size_combo.setCurrentText('14')
        layout.addWidget(self.font_size_combo)

        add_text_button = QPushButton("Add Text to Scene")
        add_text_button.clicked.connect(self.add_text_to_scene)
        layout.addWidget(add_text_button)

    def setup_connections(self):
        # Toolbar connections
        self.toolbar.open_image.connect(self.editor_widget.load_image)
        self.toolbar.save_image.connect(self.editor_widget.save_image)
        self.toolbar.rotate_image.connect(self.editor_widget.rotate_image)
        self.toolbar.flip_horizontal.connect(self.editor_widget.flip_image_horizontal)
        self.toolbar.flip_vertical.connect(self.editor_widget.flip_image_vertical)
        self.toolbar.enable_crop.connect(self.editor_widget.enable_crop)
        self.toolbar.enable_draw.connect(self.editor_widget.enable_drawing)
        self.toolbar.zoom_in.connect(self.editor_widget.zoom_in)
        self.toolbar.zoom_out.connect(self.editor_widget.zoom_out)

        # Frame settings connections
        self.format_combo.currentTextChanged.connect(self.editor_widget.set_frame_format)
        self.width_slider.valueChanged.connect(self.editor_widget.set_frame_width)

        # Image adjustment connections
        self.brightness_slider.valueChanged.connect(self.editor_widget.adjust_brightness)
        self.contrast_slider.valueChanged.connect(self.editor_widget.adjust_contrast)
        self.grayscale_intensity_slider.valueChanged.connect(self.editor_widget.adjust_grayscale_intensity)
        self.sepia_intensity_slider.valueChanged.connect(self.editor_widget.adjust_sepia_intensity)

    def add_text_to_scene(self):
        scene_name = self.scene_name_input.text()
        scene_description = self.scene_description_input.toPlainText()
        font_size = int(self.font_size_combo.currentText())
        self.editor_widget.add_text_to_scene(scene_name, scene_description, font_size)