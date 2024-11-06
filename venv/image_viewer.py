from PyQt5.QtWidgets import QApplication,QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QLabel, QCheckBox, QScrollArea, QWidget, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import os
import sys
class ImageGridApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("MV | Printing Software")
        self.resize(1200, 800)  # Set window size first
        self.center()
        self.load_styles("main.qss")
        self.selected_images = []  # To store selected image paths

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

        self.image_paths = []  # List to store image paths
        self.image_widgets = []  # List to store image containers
        self.image_favorites = {}  # Dictionary to track favorites

        self.image_collections = {}  # Store collections as {collection_name: [(path, favorite)]}

        self.load_saved_images()

    def center(self):
        """Center the window on the screen."""
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_styles(self, filename):
        """Load styles from a QSS file and apply them to the application."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

    def load_saved_images(self):
        """Load previously saved image paths from a file and display them."""
        if os.path.exists("images.txt"):
            current_collection = None
            with open("images.txt", "r") as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    if not line.startswith("C:/"):  # Assuming paths start with 'C:/'
                        current_collection = line
                        self.image_collections[current_collection] = []
                    else:
                        if ',' in line:
                            path, is_favorite = line.rsplit(',', 1)
                            if os.path.exists(path):
                                self.image_collections[current_collection].append((path, is_favorite == 'True'))
            self.arrange_images_in_grid()

    def import_images(self):
        """Open a file dialog to select and import multiple images."""
        image_paths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if image_paths:
            for image_path in image_paths:
                if image_path not in self.image_paths:
                    self.image_paths.append(image_path)
                    self.image_favorites[image_path] = False
                    image_container = self.create_image_container(image_path, False)
                    self.image_widgets.append(image_container)
            self.save_image_paths()
            self.arrange_images_in_grid()

    def create_image_container(self, image_path, is_favorite=False):
        """Create a container for an image with buttons for actions."""
        FRAME_WIDTH = 384
        FRAME_HEIGHT = 576
        container = QWidget()
        container.setFixedSize(FRAME_WIDTH, FRAME_HEIGHT)

        layout = QVBoxLayout(container)
        image_label = QLabel(self)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        checkbox = QCheckBox("Select", container)
        checkbox.setChecked(is_favorite)
        layout.addWidget(checkbox)

        # Add a button to toggle favorite
        favorite_button = QPushButton("Toggle Favorite", container)
        favorite_button.clicked.connect(lambda: self.toggle_favorite(image_path, favorite_button))
        layout.addWidget(favorite_button)

        # Add a button to delete the image
        delete_button = QPushButton("Delete Image", container)
        delete_button.clicked.connect(lambda: self.delete_image_container(container))
        layout.addWidget(delete_button)

        return container

    def toggle_favorite(self, image_path, favorite_button):
        """Toggle the favorite status of the image."""
        current_status = self.image_favorites.get(image_path, False)
        new_status = not current_status
        self.image_favorites[image_path] = new_status
        favorite_button.setText("Remove Favorite" if new_status else "Toggle Favorite")
        self.save_image_paths()

    def delete_image_container(self, container):
        """Remove an image container."""
        index = self.image_widgets.index(container)
        self.image_widgets.pop(index)
        self.image_paths.pop(index)
        self.grid_layout.removeWidget(container)
        container.deleteLater()
        self.save_image_paths()
        self.arrange_images_in_grid()

    def save_image_paths(self):
        """Save the list of image paths and their favorite status."""
        with open("images.txt", "w") as file:
            for collection_name, images in self.image_collections.items():
                file.write(f"{collection_name}\n")
                for path, is_favorite in images:
                    file.write(f"{path},{is_favorite}\n")

    def arrange_images_in_grid(self):
        """Arrange image containers dynamically in a grid layout."""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        row, col = 0, 0
        num_columns = 3
        for container in self.image_widgets:
            self.grid_layout.addWidget(container, row, col)
            col += 1
            if col >= num_columns:
                col = 0
                row += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGridApp()
    window.show()
    sys.exit(app.exec_())
