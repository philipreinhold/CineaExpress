from PySide6.QtWidgets import QMainWindow, QFileDialog, QVBoxLayout, QWidget, QToolBar
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from src.ui.editor_widget import EditorWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cinea_express")
        self.setGeometry(100, 100, 800, 600)

        # Editor Widget
        self.editor_widget = EditorWidget(self)
        self.setCentralWidget(self.editor_widget)

        # Create Actions
        self.create_actions()

        # Create Menu Bar
        self.create_menu_bar()

        # Create Tool Bar
        self.create_tool_bar()

    def create_actions(self):
        """Erstellt die Aktionen für die Menüleiste und die Werkzeugleiste."""
        self.open_action = QAction(QIcon.fromTheme("document-open"), "Open", self)
        self.open_action.triggered.connect(self.open_image)

        self.rotate_action = QAction(QIcon.fromTheme("object-rotate-right"), "Rotate", self)
        self.rotate_action.triggered.connect(self.rotate_image)

        self.flip_horizontal_action = QAction(QIcon.fromTheme("object-flip-horizontal"), "Flip Horizontal", self)
        self.flip_horizontal_action.triggered.connect(self.flip_image_horizontal)

        self.flip_vertical_action = QAction(QIcon.fromTheme("object-flip-vertical"), "Flip Vertical", self)
        self.flip_vertical_action.triggered.connect(self.flip_image_vertical)

    def create_menu_bar(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(self.open_action)

    def create_tool_bar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.rotate_action)
        toolbar.addAction(self.flip_horizontal_action)
        toolbar.addAction(self.flip_vertical_action)

    def open_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.editor_widget.load_image(file_name)

    def rotate_image(self):
        self.editor_widget.rotate_image()

    def flip_image_horizontal(self):
        self.editor_widget.flip_image_horizontal()

    def flip_image_vertical(self):
        self.editor_widget.flip_image_vertical()
