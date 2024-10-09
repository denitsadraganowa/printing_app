from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QPixmap
from PIL import Image
import sys
import io

class ImageApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Image Upload App")
        self.setGeometry(100, 100, 800, 600)

        # Central widget and layout
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        # QLabel to display the image
        self.image_label = QLabel("Upload an image to display", self)
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(600, 400)  # Set a default size for the image display
        self.layout.addWidget(self.image_label)

        # Upload button
        self.upload_button = QPushButton("Upload Image", self)
        self.upload_button.clicked.connect(self.open_image)  # Connect button to the open_image method
        self.layout.addWidget(self.upload_button)

        # Set the central widget layout
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def open_image(self):
        """Open a file dialog to choose an image and display it."""
        # Open a file dialog to select the image file
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")

        if image_path:
            # Open the image using PIL
            image = Image.open(image_path)

            # Convert to a format compatible with QPixmap
            image = image.convert("RGBA")  # Ensure the image is in RGBA mode
            byte_array = io.BytesIO()
            image.save(byte_array, format='PNG')
            byte_array.seek(0)

            # Create a QPixmap from the byte array
            pixmap = QPixmap()
            pixmap.loadFromData(byte_array.getvalue())

            # Display the image in the QLabel
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)  # Scale image to fit the QLabel size
# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# class ImageEditor(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.image = None
#         self.original_image = None  # To keep track of the original image for reset or other uses

#         self.init_ui()

#     def init_ui(self):
#         self.image_label = QLabel(self)
#         self.image_label.setAlignment(Qt.AlignCenter)

#         # Central widget
#         central_widget = QWidget()
#         layout = QVBoxLayout()
#         layout.addWidget(self.image_label)
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#         # Create actions for the menu
#         open_action = QAction("&Open", self)
#         open_action.triggered.connect(self.open_image)

#         save_action = QAction("&Save", self)
#         save_action.triggered.connect(self.save_image)

#         resize_action = QAction("&Resize", self)
#         resize_action.triggered.connect(self.resize_image)

#         rotate_action = QAction("&Rotate", self)
#         rotate_action.triggered.connect(self.rotate_image)

#         flip_action = QAction("&Flip", self)
#         flip_action.triggered.connect(self.flip_image)

#         grayscale_action = QAction("&Grayscale", self)
#         grayscale_action.triggered.connect(self.apply_grayscale)

#         blur_action = QAction("&Blur", self)
#         blur_action.triggered.connect(self.apply_blur)

#         sharpen_action = QAction("&Sharpen", self)
#         sharpen_action.triggered.connect(self.apply_sharpen)

#         fit_in_action = QAction("Fit &In", self)
#         fit_in_action.triggered.connect(self.fit_in)

#         fit_out_action = QAction("Fit &Out", self)
#         fit_out_action.triggered.connect(self.fit_out)

#         # Create a menu bar
#         menu_bar = self.menuBar()
#         file_menu = menu_bar.addMenu("&File")
#         file_menu.addAction(open_action)
#         file_menu.addAction(save_action)

#         edit_menu = menu_bar.addMenu("&Edit")
#         edit_menu.addAction(resize_action)
#         edit_menu.addAction(rotate_action)
#         edit_menu.addAction(flip_action)

#         filter_menu = menu_bar.addMenu("&Filters")
#         filter_menu.addAction(grayscale_action)
#         filter_menu.addAction(blur_action)
#         filter_menu.addAction(sharpen_action)

#         view_menu = menu_bar.addMenu("&View")
#         view_menu.addAction(fit_in_action)
#         view_menu.addAction(fit_out_action)

#         self.setWindowTitle("Image Editor")
#         self.resize(800, 600)

#     def open_image(self):
#         file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg)")
#         if file_name:
#             self.image = Image.open(file_name)
#             self.original_image = self.image.copy()  # Store the original image
#             self.display_image()

#     def save_image(self):
#         if self.image:
#             file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp)")
#             if file_name:
#                 self.image.save(file_name)
# ######
#     def display_image(self):
#         """Display the Pillow image in the QLabel."""
#         if self.image:
#             qt_image = PQ.ImageQt(self.image)  # Corrected the usage of ImageQt class
#             pixmap = QPixmap.fromImage(qt_image)
#             self.image_label.setPixmap(pixmap)

#     def resize_image(self):
#         if self.image:
#             new_width, new_height = 400, 300  # Example resize size (You can take user input here)
#             self.image = self.image.resize((new_width, new_height))
#             self.display_image()

#     def rotate_image(self):
#         if self.image:
#             self.image = self.image.rotate(90)  # Rotate 90 degrees
#             self.display_image()

#     def flip_image(self):
#         if self.image:
#             self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
#             self.display_image()

#     def apply_grayscale(self):
#         if self.image:
#             self.image = self.image.convert("L")  # Convert to grayscale
#             self.display_image()

#     def apply_blur(self):
#         if self.image:
#             self.image = self.image.filter(ImageFilter.BLUR)
#             self.display_image()

#     def apply_sharpen(self):
#         if self.image:
#             self.image = self.image.filter(ImageFilter.SHARPEN)
#             self.display_image()

#     def fit_in(self):
#         """Fit the image into the window size."""
#         if self.image:
#             label_size = self.image_label.size()
#             self.image = self.original_image.copy()
#             self.image.thumbnail((label_size.width(), label_size.height()))
#             self.display_image()

#     def fit_out(self):
#         """Reset the image to its original size (zoom out)."""
#         if self.image:
#             self.image = self.original_image.copy()  # Reset to original image
#             self.display_image()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     editor = ImageEditor()
#     editor.show()
#     sys.exit(app.exec_())
