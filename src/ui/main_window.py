from PySide6.QtWidgets import (QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, 
                               QWidget, QToolBar, QPushButton, QLabel, QSlider, 
                               QComboBox, QColorDialog, QLineEdit, QTextEdit, QGridLayout)
from PySide6.QtGui import QAction  # Beachte den Import von QAction hier
from PySide6.QtCore import Qt
from src.ui.editor_widget import EditorWidget
from PIL import Image

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
        
        # Bestehende Funktionen
        self.filter_box = self.create_filter_box()
        sidebar_layout.addWidget(self.filter_box)
        
        self.tool_box = self.create_tool_box()
        sidebar_layout.addWidget(self.tool_box)

        # Neue Funktionen
        self.add_frame_settings(sidebar_layout)
        self.add_zoom_settings(sidebar_layout)
        self.add_text_settings(sidebar_layout)
        self.add_frame_joystick(sidebar_layout)

        main_layout.addWidget(sidebar)

        # Metadatenanzeige
        self.metadata_label = QLabel("Metadata: ")
        self.metadata_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.5); padding: 5px;")
        self.metadata_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.editor_widget.graphics_scene.addWidget(self.metadata_label)

        self.create_tool_bar()
        self.create_menu_bar()

        # Stil anpassen
        self.apply_dieter_rams_style()

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction("🗁 Open", self)
        open_action.triggered.connect(self.open_image)
        save_action = QAction("💾 Save", self)
        save_action.triggered.connect(self.save_image)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

    def create_tool_bar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        actions = [
            ("🗁 Open", self.open_image),
            ("💾 Save", self.save_image),
            ("↻ Rotate", self.editor_widget.rotate_image),
            ("⇋ Flip H", self.editor_widget.flip_image_horizontal),
            ("⇅ Flip V", self.editor_widget.flip_image_vertical),
            ("✂ Crop", self.editor_widget.enable_crop),
            ("🔍➕ Zoom In", self.editor_widget.zoom_in),
            ("🔍➖ Zoom Out", self.editor_widget.zoom_out),
        ]

        for text, slot in actions:
            action = QAction(text, self)
            action.triggered.connect(slot)
            toolbar.addAction(action)

    def create_filter_box(self):
        filter_box = QWidget()
        filter_layout = QVBoxLayout(filter_box)

        brightness_label = QLabel("Brightness")
        brightness_slider = QSlider(Qt.Horizontal)
        brightness_slider.setRange(-100, 100)
        brightness_slider.setValue(0)
        brightness_slider.valueChanged.connect(self.editor_widget.adjust_brightness)

        contrast_label = QLabel("Contrast")
        contrast_slider = QSlider(Qt.Horizontal)
        contrast_slider.setRange(-100, 100)
        contrast_slider.setValue(0)
        contrast_slider.valueChanged.connect(self.editor_widget.adjust_contrast)

        grayscale_label = QLabel("Grayscale Intensity")
        grayscale_slider = QSlider(Qt.Horizontal)
        grayscale_slider.setRange(0, 100)
        grayscale_slider.setValue(0)
        grayscale_slider.valueChanged.connect(self.editor_widget.adjust_grayscale_intensity)

        sepia_label = QLabel("Sepia Intensity")
        sepia_slider = QSlider(Qt.Horizontal)
        sepia_slider.setRange(0, 100)
        sepia_slider.setValue(0)
        sepia_slider.valueChanged.connect(self.editor_widget.adjust_sepia_intensity)

        filter_layout.addWidget(brightness_label)
        filter_layout.addWidget(brightness_slider)
        filter_layout.addWidget(contrast_label)
        filter_layout.addWidget(contrast_slider)
        filter_layout.addWidget(grayscale_label)
        filter_layout.addWidget(grayscale_slider)
        filter_layout.addWidget(sepia_label)
        filter_layout.addWidget(sepia_slider)

        return filter_box

    def create_tool_box(self):
        tool_box = QWidget()
        tool_layout = QVBoxLayout(tool_box)

        format_label = QLabel("Select Format")
        format_dropdown = QComboBox()
        formats = ["16:9", "4:3", "1.85:1", "2.35:1", "1:1", "9:16"]
        format_dropdown.addItems(formats)
        format_dropdown.currentTextChanged.connect(self.editor_widget.set_frame_format)

        line_width_label = QLabel("Line Width")
        line_width_slider = QSlider(Qt.Horizontal)
        line_width_slider.setRange(1, 10)
        line_width_slider.setValue(2)
        line_width_slider.valueChanged.connect(self.editor_widget.set_frame_pen_width)

        line_color_button = QPushButton("Choose Line Color")
        line_color_button.clicked.connect(self.editor_widget.set_frame_color)

        tool_layout.addWidget(format_label)
        tool_layout.addWidget(format_dropdown)
        tool_layout.addWidget(line_width_label)
        tool_layout.addWidget(line_width_slider)
        tool_layout.addWidget(line_color_button)

        return tool_box

    def add_frame_settings(self, layout):
        frame_label = QLabel("Frame Settings")
        frame_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(frame_label)

        self.frame_width_slider = QSlider(Qt.Horizontal)
        self.frame_width_slider.setRange(10, 100)  # 10% bis 100% der maximalen Breite
        self.frame_width_slider.setValue(80)  # Standardmäßig 80%
        self.frame_width_slider.valueChanged.connect(self.update_frame)
        layout.addWidget(QLabel("Frame Size"))
        layout.addWidget(self.frame_width_slider)

    def add_zoom_settings(self, layout):
        zoom_label = QLabel("Zoom")
        zoom_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(zoom_label)

        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setRange(50, 200)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.editor_widget.set_zoom)
        layout.addWidget(self.zoom_slider)

    def add_text_settings(self, layout):
        text_label = QLabel("Scene Text")
        text_label.setStyleSheet("color: white; font-weight: bold;")
        layout.addWidget(text_label)

        self.scene_name_input = QLineEdit()
        self.scene_name_input.setPlaceholderText("Scene Name")
        layout.addWidget(self.scene_name_input)

        self.scene_description_input = QTextEdit()
        self.scene_description_input.setPlaceholderText("Scene Description")
        layout.addWidget(self.scene_description_input)

        add_text_button = QPushButton("Add Text to Scene")
        add_text_button.clicked.connect(self.add_text_to_scene)
        layout.addWidget(add_text_button)

    def add_frame_joystick(self, layout):
        joystick_layout = QGridLayout()
        up_button = QPushButton("↑")
        down_button = QPushButton("↓")
        left_button = QPushButton("←")
        right_button = QPushButton("→")

        joystick_layout.addWidget(up_button, 0, 1)
        joystick_layout.addWidget(left_button, 1, 0)
        joystick_layout.addWidget(right_button, 1, 2)
        joystick_layout.addWidget(down_button, 2, 1)

        up_button.clicked.connect(lambda: self.editor_widget.move_frame(0, -10))
        down_button.clicked.connect(lambda: self.editor_widget.move_frame(0, 10))
        left_button.clicked.connect(lambda: self.editor_widget.move_frame(-10, 0))
        right_button.clicked.connect(lambda: self.editor_widget.move_frame(10, 0))

        layout.addLayout(joystick_layout)

    def update_frame(self):
        width_percentage = self.frame_width_slider.value()
        self.editor_widget.set_frame_width(width_percentage)

    def add_text_to_scene(self):
        scene_name = self.scene_name_input.text()
        scene_description = self.scene_description_input.toPlainText()
        self.editor_widget.add_text_to_scene(scene_name, scene_description)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        print(f"Selected file: {file_name}")  # Debug-Ausgabe
        if file_name:
            try:
                self.editor_widget.load_image(file_name)
                self.update_metadata(file_name)
            except Exception as e:
                print(f"Error loading image: {str(e)}")  # Debug-Ausgabe

    def save_image(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if output_path:
            self.editor_widget.save_image(output_path)

    def update_metadata(self, image_path):
        image = Image.open(image_path)
        metadata = f"Metadata: {image.format}, {image.size}, {image.mode}"
        self.metadata_label.setText(metadata)
        self.metadata_label.adjustSize()
        self.metadata_label.move(10, self.editor_widget.graphics_view.height() - self.metadata_label.height() - 10)

    def apply_dieter_rams_style(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2C2C2C;
                color: white;
                font-family: Arial;
            }
            QPushButton {
                background-color: #3C3C3C;
                border: 1px solid white;
                border-radius: 5px;
                padding: 5px;
            }
            QSlider::handle:horizontal {
                background-color: orange;
                border: 1px solid white;
                width: 18px;
                margin: -2px 0;
                border-radius: 3px;
            }
        """)