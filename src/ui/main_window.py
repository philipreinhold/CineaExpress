from PySide6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QToolBar, QPushButton, QLabel, QSlider, QComboBox, QColorDialog
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from src.ui.editor_widget import EditorWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinea_express")
        self.setGeometry(100, 100, 1200, 800)

        # Hauptlayout: Horizontale Aufteilung für Seitenleisten und Editor
        main_layout = QHBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Editor Widget
        self.editor_widget = EditorWidget(self)
        main_layout.addWidget(self.editor_widget, stretch=3)

        # Linke Seitenleiste für Farb- und Filteroptionen
        self.filter_box = self.create_filter_box()
        main_layout.addWidget(self.filter_box, stretch=1)

        # Rechte Seitenleiste für Bildbearbeitungswerkzeuge
        self.tool_box = self.create_tool_box()
        main_layout.addWidget(self.tool_box, stretch=1)

        # Metadatenanzeige im Bildrahmen unten
        self.metadata_label = QLabel("Metadata: ")
        self.metadata_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 0.5); padding: 5px;")
        self.metadata_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.editor_widget.graphics_scene.addWidget(self.metadata_label)

        # Create Tool Bar
        self.create_tool_bar()

        # Create Menu Bar
        self.create_menu_bar()

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

        open_action = QAction("🗁 Open", self)
        open_action.triggered.connect(self.open_image)

        save_action = QAction("💾 Save", self)
        save_action.triggered.connect(self.save_image)

        draw_action = QAction("✏️ Draw", self)
        draw_action.triggered.connect(self.editor_widget.enable_drawing)

        color_action = QAction("🎨 Color", self)
        color_action.triggered.connect(self.editor_widget.change_pen_color)

        toolbar.addAction(open_action)
        toolbar.addAction(save_action)
        toolbar.addAction(draw_action)
        toolbar.addAction(color_action)

    def create_tool_box(self):
        """Erstellt eine Seitenleiste mit Buttons für Bildbearbeitungswerkzeuge und Framing-Optionen."""
        tool_box = QVBoxLayout()

        rotate_button = QPushButton("↻ Rotate")
        rotate_button.clicked.connect(self.editor_widget.rotate_image)

        flip_horizontal_button = QPushButton("⇋ Flip H")
        flip_horizontal_button.clicked.connect(self.editor_widget.flip_image_horizontal)

        flip_vertical_button = QPushButton("⇅ Flip V")
        flip_vertical_button.clicked.connect(self.editor_widget.flip_image_vertical)

        crop_button = QPushButton("✂ Crop")
        crop_button.clicked.connect(self.editor_widget.enable_crop)

        zoom_in_button = QPushButton("🔍➕ Zoom In")
        zoom_in_button.clicked.connect(self.editor_widget.zoom_in)

        zoom_out_button = QPushButton("🔍➖ Zoom Out")
        zoom_out_button.clicked.connect(self.editor_widget.zoom_out)

        tool_box.addWidget(rotate_button)
        tool_box.addWidget(flip_horizontal_button)
        tool_box.addWidget(flip_vertical_button)
        tool_box.addWidget(crop_button)
        tool_box.addWidget(zoom_in_button)
        tool_box.addWidget(zoom_out_button)

        # Dropdown für das Format
        format_label = QLabel("Select Format")
        format_dropdown = QComboBox()
        formats = [
            "16:9", "4:3", "1.85:1", "2.35:1", "1.33:1", "2.39:1", "9:16",
            "1.66:1", "3:2", "1.78:1", "5:4", "1.375:1", "2.76:1", "2:1",
            "1.9:1", "1.43:1", "1.50:1", "1.25:1", "1.21:1", "1.2:1"
        ]
        format_dropdown.addItems(formats)
        format_dropdown.currentTextChanged.connect(self.editor_widget.set_frame_format)

        # Schieberegler für Linienbreite
        line_width_label = QLabel("Line Width")
        line_width_slider = QSlider(Qt.Horizontal)
        line_width_slider.setRange(1, 10)
        line_width_slider.setValue(2)
        line_width_slider.valueChanged.connect(self.editor_widget.set_frame_pen_width)

        # Button für Linienfarbe
        line_color_button = QPushButton("Choose Line Color")
        line_color_button.clicked.connect(self.editor_widget.set_frame_color)

        # Dropdown für Linienstil
        line_style_dropdown = QComboBox()
        line_style_dropdown.addItem("Solid", Qt.SolidLine)
        line_style_dropdown.addItem("Dashed", Qt.DashLine)
        line_style_dropdown.currentIndexChanged.connect(
            lambda index: self.editor_widget.set_frame_style(line_style_dropdown.itemData(index))
        )

        tool_box.addWidget(format_label)
        tool_box.addWidget(format_dropdown)
        tool_box.addWidget(line_width_label)
        tool_box.addWidget(line_width_slider)
        tool_box.addWidget(line_color_button)
        tool_box.addWidget(line_style_dropdown)

        tool_box.addStretch()

        tool_container = QWidget()
        tool_container.setLayout(tool_box)

        return tool_container

    def create_filter_box(self):
        """Erstellt eine Seitenleiste mit Schiebereglern für Farb- und Filteroptionen."""
        filter_box = QVBoxLayout()

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

        filter_box.addWidget(brightness_label)
        filter_box.addWidget(brightness_slider)
        filter_box.addWidget(contrast_label)
        filter_box.addWidget(contrast_slider)
        filter_box.addWidget(grayscale_label)
        filter_box.addWidget(grayscale_slider)
        filter_box.addWidget(sepia_label)
        filter_box.addWidget(sepia_slider)
        filter_box.addStretch()

        filter_container = QWidget()
        filter_container.setLayout(filter_box)

        return filter_container

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.editor_widget.load_image(file_name)
            self.update_metadata(file_name)

    def save_image(self):
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if output_path:
            self.editor_widget.save_image(output_path)

    def update_metadata(self, image_path):
        from PIL import Image
        image = Image.open(image_path)
        metadata = f"Metadata: {image.format}, {image.size}, {image.mode}"
        self.metadata_label.setText(metadata)
        self.metadata_label.adjustSize()
        self.metadata_label.move(10, self.graphics_view.height() - self.metadata_label.height() - 10)
