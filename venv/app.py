

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance
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

        # Add sliders for color adjustments
        self.create_color_sliders()

        # Create Fit In and Fit Out buttons
        self.create_fit_buttons()

        # Set the central widget layout
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.image = None  # Store the current image
        self.original_pixmap = None  # Store the original pixmap for resizing

    def create_color_sliders(self):
        """Create sliders for color adjustments."""
        # Create a layout for sliders
        slider_layout = QVBoxLayout()

        # Yellow/Blue slider
        self.yellow_blue_slider = QSlider()
        self.yellow_blue_slider.setOrientation(1)  # Horizontal
        self.yellow_blue_slider.setRange(-100, 100)
        self.yellow_blue_slider.setValue(0)
        self.yellow_blue_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.yellow_blue_slider)

        # Magenta/Green slider
        self.magenta_green_slider = QSlider()
        self.magenta_green_slider.setOrientation(1)  # Horizontal
        self.magenta_green_slider.setRange(-100, 100)
        self.magenta_green_slider.setValue(0)
        self.magenta_green_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.magenta_green_slider)

        # Cyan/Red slider
        self.cyan_red_slider = QSlider()
        self.cyan_red_slider.setOrientation(1)  # Horizontal
        self.cyan_red_slider.setRange(-100, 100)
        self.cyan_red_slider.setValue(0)
        self.cyan_red_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.cyan_red_slider)

        # Brightness/Darkness slider
        self.brightness_slider = QSlider()
        self.brightness_slider.setOrientation(1)  # Horizontal
        self.brightness_slider.setRange(0, 200)
        self.brightness_slider.setValue(100)  # Start with normal brightness
        self.brightness_slider.valueChanged.connect(self.update_image)
        slider_layout.addWidget(self.brightness_slider)

        # Add sliders layout to the main layout
        self.layout.addLayout(slider_layout)

    def create_fit_buttons(self):
        """Create Fit In and Fit Out buttons."""
        fit_layout = QHBoxLayout()

        # Fit In button
        self.fit_in_button = QPushButton("Fit In")
        self.fit_in_button.clicked.connect(self.fit_in)
        fit_layout.addWidget(self.fit_in_button)

        # Fit Out button
        self.fit_out_button = QPushButton("Fit Out")
        self.fit_out_button.clicked.connect(self.fit_out)
        fit_layout.addWidget(self.fit_out_button)

        # Add fit buttons layout to the main layout
        self.layout.addLayout(fit_layout)

    def open_image(self):
        """Open a file dialog to choose an image and display it."""
        # Open a file dialog to select the image file
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.jpeg)")

        if image_path:
            # Open the image using PIL
            self.image = Image.open(image_path)
            self.original_pixmap = self.image_to_pixmap(self.image)  # Save the original pixmap
            self.display_image(self.original_pixmap)

    def display_image(self, pixmap):
        """Display the given QPixmap in the QLabel."""
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)  # Scale image to fit the QLabel size

    def image_to_pixmap(self, image):
        """Convert a PIL image to QPixmap."""
        image = image.convert("RGBA")  # Ensure the image is in RGBA mode
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)

        # Create a QPixmap from the byte array
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.getvalue())
        return pixmap

    def fit_in(self):
        """Fit the image in the QLabel while maintaining aspect ratio."""
        if self.original_pixmap:
            self.image_label.setPixmap(self.original_pixmap.scaled(self.image_label.size(), aspectRatioMode=True, transformMode=0))

    def fit_out(self):
        """Fit the QLabel to the pixmap, which may crop the image."""
        if self.original_pixmap:
            self.image_label.setPixmap(self.original_pixmap.scaled(self.image_label.size(), aspectRatioMode=False, transformMode=0))

    def update_image(self):
        """Update the image based on the current slider values."""
        if self.image:
            # Create a copy of the original image
            modified_image = self.image.copy()

            # Adjust yellow/blue
            yellow_blue_value = self.yellow_blue_slider.value()
            modified_image = self.apply_yellow_blue_tint(modified_image, yellow_blue_value)

            # Adjust magenta/green
            magenta_green_value = self.magenta_green_slider.value()
            modified_image = self.apply_magenta_green_tint(modified_image, magenta_green_value)

            # Adjust cyan/red
            cyan_red_value = self.cyan_red_slider.value()
            modified_image = self.apply_cyan_red_tint(modified_image, cyan_red_value)

            # Adjust brightness
            brightness_value = self.brightness_slider.value() / 100.0  # Scale to range 0.0 - 2.0
            modified_image = ImageEnhance.Brightness(modified_image).enhance(brightness_value)

            # Convert modified image to QPixmap and display it
            self.display_image(self.image_to_pixmap(modified_image))

    def apply_yellow_blue_tint(self, image, value):
        """Apply yellow/blue tint based on the value."""
        r, g, b = image.split()
        r = r.point(lambda i: i + value)  # Increase red for yellow, decrease for blue
        return Image.merge("RGB", (r, g, b))

    def apply_magenta_green_tint(self, image, value):
        """Apply magenta/green tint based on the value."""
        r, g, b = image.split()
        g = g.point(lambda i: i + value)  # Increase green for green, decrease for magenta
        return Image.merge("RGB", (r, g, b))

    def apply_cyan_red_tint(self, image, value):
        """Apply cyan/red tint based on the value."""
        r, g, b = image.split()
        b = b.point(lambda i: i + value)  # Increase blue for cyan, decrease for red
        return Image.merge("RGB", (r, g, b))

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = ImageApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

