from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance
import sys
import io

class ImageEditorApp(QMainWindow):
    image_saved = pyqtSignal(str)  # Signal to emit the saved image path

    def __init__(self, image_path):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Image Editor")
        self.setGeometry(100, 100, 800, 600)

        # Store the image path for saving purposes
        self.image_path = image_path

        # Create a central widget and layout
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.main_layout.addWidget(self.image_label)

        # Load and display the image
        self.original_image = Image.open(image_path)
        self.image = self.original_image.copy()
        self.display_image()

        # Create buttons and sliders for image editing
        self.create_controls()

        self.setCentralWidget(self.central_widget)

    def display_image(self):
        """Display the image in the label."""
        pixmap = self.image_to_pixmap(self.image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(600, 400)  # Set a standard size for the displayed image

    def image_to_pixmap(self, image):
        """Convert a PIL image to QPixmap."""
        image = image.convert("RGBA")  # Ensure the image is in RGBA mode
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.getvalue())
        return pixmap

    def create_controls(self):
        """Create control buttons and sliders for image editing."""
        # Slider layout
        slider_layout = QHBoxLayout()

        # Brightness slider
        self.brightness_slider = QSlider()
        self.brightness_slider.setOrientation(1)  # Horizontal
        self.brightness_slider.setRange(0, 200)
        self.brightness_slider.setValue(100)  # Start with normal brightness
        self.brightness_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.brightness_slider)

        # Contrast slider
        self.contrast_slider = QSlider()
        self.contrast_slider.setOrientation(1)  # Horizontal
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)  # Start with normal contrast
        self.contrast_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.contrast_slider)

        # Saturation slider
        self.saturation_slider = QSlider()
        self.saturation_slider.setOrientation(1)  # Horizontal
        self.saturation_slider.setRange(0, 200)
        self.saturation_slider.setValue(100)  # Start with normal saturation
        self.saturation_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.saturation_slider)

        # Sharpness slider
        self.sharpness_slider = QSlider()
        self.sharpness_slider.setOrientation(1)  # Horizontal
        self.sharpness_slider.setRange(0, 200)
        self.sharpness_slider.setValue(100)  # Start with normal sharpness
        self.sharpness_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.sharpness_slider)

        # Create Rotate buttons
        self.rotate_left_button = QPushButton("Rotate Left")
        self.rotate_left_button.clicked.connect(self.rotate_left)

        self.rotate_right_button = QPushButton("Rotate Right")
        self.rotate_right_button.clicked.connect(self.rotate_right)

        # Create Fit In/Out buttons
        self.fit_in_button = QPushButton("Fit In")
        self.fit_in_button.clicked.connect(self.fit_in)

        self.fit_out_button = QPushButton("Fit Out")
        self.fit_out_button.clicked.connect(self.fit_out)

        # Apply Changes button
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self.apply_changes)

        # Add all controls to the layout
        self.main_layout.addLayout(slider_layout)
        self.main_layout.addWidget(self.rotate_left_button)
        self.main_layout.addWidget(self.rotate_right_button)
        self.main_layout.addWidget(self.fit_in_button)
        self.main_layout.addWidget(self.fit_out_button)
        self.main_layout.addWidget(self.apply_button)

    def update_image(self):
        """Update the image based on the current slider values."""
        brightness_value = self.brightness_slider.value() / 100.0
        contrast_value = self.contrast_slider.value() / 100.0
        saturation_value = self.saturation_slider.value() / 100.0
        sharpness_value = self.sharpness_slider.value() / 100.0

        # Apply adjustments to the image
        image = ImageEnhance.Brightness(self.original_image).enhance(brightness_value)
        image = ImageEnhance.Contrast(image).enhance(contrast_value)
        image = ImageEnhance.Color(image).enhance(saturation_value)
        self.image = ImageEnhance.Sharpness(image).enhance(sharpness_value)

        self.display_image()

    def rotate_left(self):
        """Rotate the image left by 90 degrees."""
        self.image = self.image.rotate(90, expand=True)
        self.display_image()

    def rotate_right(self):
        """Rotate the image right by 90 degrees."""
        self.image = self.image.rotate(-90, expand=True)
        self.display_image()

    def fit_in(self):
        """Zoom out of the image."""
        width, height = self.image.size
        self.image = self.image.resize((int(width * 0.8), int(height * 0.8)), Image.ANTIALIAS)
        self.display_image()

    def fit_out(self):
        """Zoom in on the image."""
        width, height = self.image.size
        self.image = self.image.resize((int(width * 1.2), int(height * 1.2)), Image.ANTIALIAS)
        self.display_image()

    def apply_changes(self):
        """Save the modified image, emit the signal, and close the window."""
        self.image.save(self.image_path)  # Save the modified image
        self.image_saved.emit(self.image_path)  # Emit signal to notify the main application
        self.close()  # Close the editor window

# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditorApp("path_to_your_image.jpg")  # Replace with the actual image path
    editor.image_saved.connect(lambda path: print(f"Image saved at {path}"))  # Temporary for testing
    editor.show()
    sys.exit(app.exec_())

