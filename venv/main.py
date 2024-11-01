

from PyQt5.QtWidgets import QApplication, QMainWindow, QSpacerItem, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QWidget, QScrollArea, QSizePolicy, QFrame, QCheckBox  # Added QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt5.QtCore import Qt, QSize

import sys
from edit import ImageEditorApp  # Import the ImageEditorApp class from edit.py
from PyQt5.QtGui import QPixmap, QIcon 
from color import ColorEditorApp  # Import the ColorEditorApp class from color.py


class ImageGridApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("MV | Printing Software")
        self.setGeometry(1000, 1000, 1200, 800)
        self.load_styles("main.qss")

        # Central widget and main layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # Create a horizontal layout for the top section
        top_layout = QHBoxLayout()
        
        # Create spacer to push the button to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_layout.addItem(spacer)

        # Upload button to import multiple images
        self.upload_button = QPushButton(self)
        self.upload_button.setIcon(QIcon("upload.jpg"))
        self.upload_button.clicked.connect(self.import_images)

        # Add the button to the top layout
        top_layout.addWidget(self.upload_button)

        # Add the top layout to the main layout
        self.main_layout.addLayout(top_layout)

        # Create a scroll area to hold the grid layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.grid_layout = QGridLayout(self.image_container)  # Use QGridLayout for the grid of images

        # Set the scroll area widget
        self.scroll_area.setWidget(self.image_container)
        self.main_layout.addWidget(self.scroll_area)

        # Set the central widget layout
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.image_widgets = []  # Store references to image containers for layout management
        self.selected_images = []  # List to store paths of selected images

    def load_styles(self, filename):
        """Load styles from a QSS file and apply them to the application."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

    def import_images(self):
        """Open a file dialog to select and import multiple images."""
        image_paths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Images (*.png *.jpg *.jpeg *.bmp)")

        if image_paths:
            # Clear existing images and layout
            self.clear_layout()

            # Create and add image containers with buttons for each image
            for image_path in image_paths:
                image_container = self.create_image_container(image_path)
                self.image_widgets.append(image_container)

            # Dynamically arrange image containers in the grid layout
            self.arrange_images_in_grid()

    def create_image_container(self, image_path):
        container = QFrame()
        container.setFrameShape(QFrame.Box)
        container.setStyleSheet("""
            QFrame {
                background-color: #044877; 
                border: 2px solid #cccccc;
                border-radius: 15px; 
                padding: 5px;
                margin: 5px;
            }
        """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)  # Ensure no extra margin between image and buttons

        # Image label
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        target_width = 200  # Example width
        target_height = int(target_width * 1.5)  # 4:6 ratio for portrait images
        scaled_pixmap = self.fit_in(pixmap, target_width, target_height)
        image_label.setPixmap(scaled_pixmap)
        image_label.setFixedSize(target_width, target_height)

        # Add checkbox for selecting the image
        checkbox = QCheckBox(container)
        checkbox.setStyleSheet("QCheckBox { margin: 2px; }")
        checkbox.setGeometry(5, 5, 20, 20)  # Position the checkbox in the top-left corner

        # Connect checkbox toggle to update the selected images list
        checkbox.toggled.connect(lambda checked, path=image_path: self.update_selected_images(checked, path))

        container_layout.addWidget(image_label)

        # Add buttons panel (same as in the previous implementation)
        button_panel = QWidget()
        button_panel.setStyleSheet("background-color:#f5f5f5;")
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

        # Define button size
        button_size = 60

        # Create and add buttons
        download_button = QPushButton()
        download_button.setIcon(QIcon("download.jpg"))
        download_button.setIconSize(QSize(40, 40))
        edit_button = QPushButton()
        edit_button.setIcon(QIcon("edit.jpg"))
        edit_button.setIconSize(QSize(40, 40))
        palette_button = QPushButton()
        palette_button.setIcon(QIcon("palette.jpg"))
        palette_button.setIconSize(QSize(40, 40))
        favorite_button = QPushButton()
        favorite_button.setIcon(QIcon("heart.jpg"))
        favorite_button.setIconSize(QSize(40, 40))
        delete_button = QPushButton()
        delete_button.setIcon(QIcon("delete.png"))
        delete_button.setIconSize(QSize(40, 40))

        # Set button sizes and styles
        for btn in [download_button, edit_button, palette_button, favorite_button, delete_button]:
            btn.setFixedSize(button_size, button_size)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: none;
                    border-radius: 5px;
                    color: white;
                    font-size: 22px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
            """)

        # Connect the palette button to open selected images in ColorEditorApp
        palette_button.clicked.connect(self.open_selected_images_in_palette)

        # Add buttons to the button panel
        button_layout.addWidget(download_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(palette_button)
        button_layout.addWidget(favorite_button)
        button_layout.addWidget(delete_button)

        # Set the height of the button panel to match the button size
        button_panel.setFixedHeight(button_size + 10)

        # Add the button panel to the container layout, attach it closely to the image
        container_layout.addWidget(button_panel, alignment=Qt.AlignBottom)

        return container

    def update_selected_images(self, checked, path):
        """Update the list of selected images based on the checkbox state."""
        if checked:
            self.selected_images.append(path)
        else:
            self.selected_images.remove(path)

    def open_selected_images_in_palette(self):
        """Open ColorEditorApp with all selected images."""
        if not self.selected_images:  # Check if no images are selected
            return  # Do nothing or show a message
        self.color_editor = ColorEditorApp(self, self.selected_images)  # Pass the list of selected image paths
        self.color_editor.show()


    def clear_layout(self):
        """Clear the current layout of image containers."""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.image_widgets.clear()

    def arrange_images_in_grid(self):
        """Arrange image containers dynamically in a grid layout."""
        num_columns = 3  # Example column count
        row = 0
        col = 0
        for image_container in self.image_widgets:
            self.grid_layout.addWidget(image_container, row, col)
            col += 1
            if col >= num_columns:
                col = 0
                row += 1

    def fit_in(self, pixmap, target_width, target_height):
        """Resize the image to fit within the target dimensions while maintaining aspect ratio."""
        return pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    #### don't need the following 2 defs
    def refresh_images(self, image_paths):
        """Refresh the displayed images in the main window."""
        self.image_paths = image_paths  # Update with the new paths if needed
        self.display_images(self.image_paths)  # Reload and display images

    def display_images(self, image_paths):
        """Display images in the main window."""
        # Clear existing labels
        for label in self.image_labels:
            label.deleteLater()  # Clean up previous labels
        self.image_labels.clear()  # Clear the list of labels

        row, col = 0, 0
        max_columns = 3
        self.grid_layout = QGridLayout()  # Assuming you have a grid layout to display images
        self.container_widget.setLayout(self.grid_layout)  # Set the layout for your container

        for image_path in image_paths:
            if not os.path.exists(image_path):
                continue
            
            # Create a QLabel to display the image
            image_label = QLabel(self)
            pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.grid_layout.addWidget(image_label, row, col)
            self.image_labels.append(image_label)

            # Update grid placement
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGridApp()
    window.show()
    sys.exit(app.exec_())
