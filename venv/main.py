
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QWidget, QScrollArea, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal
import sys
import subprocess  # To open the other page
from edit import ImageEditorApp  # Import the ImageEditorApp class from edit.py

class ImageGridApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Image Grid with Button Panel")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget and main layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # Upload button to import multiple images
        self.upload_button = QPushButton("Upload Images", self)
        self.upload_button.clicked.connect(self.import_images)
        self.main_layout.addWidget(self.upload_button)

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

    def import_images(self):
        """Open a file dialog to select and import multiple images."""
        # Open a file dialog for multiple image selection
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
        """Create a container with an image and a button panel below it."""
        # Create a new QWidget as the container
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Create an image label and set the image
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(True)
        image_label.setFixedSize(200, 300)  # Set standard size for the image
        container_layout.addWidget(image_label)

        # Create a button panel below the image
        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setSpacing(5)  # Set spacing between buttons for better appearance

        # Create and add placeholder buttons with symbols
        download_button = QPushButton("↓")
        edit_button = QPushButton("✎")  # Edit button will open the other window
        palette_button = QPushButton("🎨")
        favorite_button = QPushButton("❤")
        delete_button = QPushButton("🗑")

        # Set fixed size for buttons to match the width of the image container
        button_width = 32
        button_height = 30
        for btn in [download_button, edit_button, palette_button, favorite_button, delete_button]:
            btn.setFixedSize(button_width, button_height)
            btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Set fixed size policy for consistent button size

        # Connect the edit button click to open the new window with the image
        edit_button.clicked.connect(lambda: self.open_image_in_new_window(image_path))

        # Add buttons to the layout
        button_layout.addWidget(download_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(palette_button)
        button_layout.addWidget(favorite_button)
        button_layout.addWidget(delete_button)

        # Add the button panel below the image
        container_layout.addWidget(button_panel)

        return container

    def open_image_in_new_window(self, image_path):
        """Open the image in the other application window (edit.py) by passing the image path."""
        self.image_editor = ImageEditorApp(image_path)
        self.image_editor.image_saved.connect(self.update_image)  # Connect signal to update image
        self.image_editor.show()

    def update_image(self, image_path):
        """Update the displayed image after editing."""
        self.clear_layout()  # Clear old images (if needed)
        # Add the edited image to the grid
        edited_container = self.create_image_container(image_path)
        self.image_widgets.append(edited_container)
        self.arrange_images_in_grid()

    def arrange_images_in_grid(self):
        """Arrange image containers in a responsive grid layout."""
        num_images = len(self.image_widgets)

        # Calculate the number of columns based on the window width
        container_width = self.image_container.width()
        image_width = 200  # Fixed width of each image container
        columns = max(1, container_width // image_width)  # Calculate the number of columns based on container width

        # Arrange image containers in rows and columns
        row, col = 0, 0
        for index, container in enumerate(self.image_widgets):
            self.grid_layout.addWidget(container, row, col)
            col += 1
            if col >= columns:  # Move to the next row if column limit is reached
                col = 0
                row += 1

    def resizeEvent(self, event):
        """Override resize event to re-arrange images on window resize."""
        super().resizeEvent(event)
        self.arrange_images_in_grid()  # Rearrange images whenever the window is resized

    def clear_layout(self):
        """Clear all image widgets from the layout."""
        for widget in self.image_widgets:
            self.grid_layout.removeWidget(widget)
            widget.deleteLater()  # Delete widget to free memory
        self.image_widgets = []

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = ImageGridApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

