from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QSizePolicy, QSlider, QPushButton, QMainWindow, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance
import io
import os
import sys

class ColorEditorApp(QMainWindow):
    def __init__(self, main_window, image_paths):
        super().__init__()

        self.main_window = main_window  # Reference to the main window
        self.setWindowTitle("Image Color Editor")
        self.setGeometry(300, 300, 1200, 800)

        # Main layout with a scroll area
        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Create a scroll area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Create a container widget to hold the grid layout
        self.container_widget = QWidget()
        self.grid_layout = QGridLayout(self.container_widget)

        # Add container widget to scroll area
        self.scroll_area.setWidget(self.container_widget)
        self.main_layout.addWidget(self.scroll_area)

        # Create sliders layout
        self.controls_layout = QVBoxLayout()

        # Display all the selected images in a grid layout
        self.display_images(image_paths)

        # Create image controls for sliders
        self.create_controls()

        # Add the "Apply Changes" button
        self.apply_button = QPushButton("Apply Changes", self)
        self.apply_button.clicked.connect(self.apply_changes)

        self.main_layout.addWidget(self.apply_button)  # Corrected to use main_layout

    def display_images(self, image_paths):
        """Display all selected images in a grid layout."""
        row, col = 0, 0
        max_columns = 3
        self.image_labels = []
        self.original_images = []
        self.current_images = []
        self.image_paths = image_paths  # Store the paths for saving later

        for image_path in image_paths:
            if not os.path.exists(image_path):
                continue

            # Load and store the original image
            original_image = Image.open(image_path)
            self.original_images.append(original_image)
            self.current_images.append(original_image.copy())

            # Create a QLabel to display the image
            image_label = QLabel(self)
            pixmap = self.image_to_pixmap(original_image)
            image_label.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=1))
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.grid_layout.addWidget(image_label, row, col)
            self.image_labels.append(image_label)

            # Update grid placement
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

    def image_to_pixmap(self, image):
        """Convert a PIL image to QPixmap."""
        image = image.convert("RGBA")
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.getvalue())
        return pixmap

    def create_controls(self):
        """Create control buttons and sliders for image editing."""
        slider_layout = QVBoxLayout()

        # Brightness slider
        self.brightness_slider = self.create_slider("Brightness", slider_layout, self.update_image)
        self.contrast_slider = self.create_slider("Contrast", slider_layout, self.update_image)
        self.saturation_slider = self.create_slider("Saturation", slider_layout, self.update_image)
        self.sharpness_slider = self.create_slider("Sharpness", slider_layout, self.update_image)

        self.main_layout.addLayout(slider_layout)

    def create_slider(self, name, layout, callback):
        """Create a slider with labels and connect it to a callback."""
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 200)
        slider.setValue(100)
        slider.valueChanged.connect(callback)

        label = QLabel(f"{name}: 100")
        slider.valueChanged.connect(lambda value: label.setText(f"{name}: {value}"))

        layout.addWidget(slider)
        layout.addWidget(label)
        return slider

    def update_image(self):
        """Update all displayed images based on the slider values."""
        brightness_value = self.brightness_slider.value() / 100.0
        contrast_value = self.contrast_slider.value() / 100.0
        saturation_value = self.saturation_slider.value() / 100.0
        sharpness_value = self.sharpness_slider.value() / 100.0

        for idx, original_image in enumerate(self.original_images):
            image = ImageEnhance.Brightness(original_image).enhance(brightness_value)
            image = ImageEnhance.Contrast(image).enhance(contrast_value)
            image = ImageEnhance.Color(image).enhance(saturation_value)
            image = ImageEnhance.Sharpness(image).enhance(sharpness_value)
            self.current_images[idx] = image

            pixmap = self.image_to_pixmap(image)
            self.image_labels[idx].setPixmap(pixmap.scaled(200, 200, aspectRatioMode=1))

    def apply_changes(self):
        """Save the modified images back to their original paths and close the editor."""
        for idx, image in enumerate(self.current_images):
            if idx < len(self.image_paths):  # Ensure we have a corresponding path
                image.save(self.image_paths[idx])  # Save the modified image to the original path

        print("Changes applied and images saved.")

        # Notify the main window
        self.main_window.status_label.setText("Changes applied and images saved.")
        self.main_window.refresh_images(self.image_paths)  # Call the refresh method with updated image paths
        self.close()  # Close the color editor window


# Main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Create an instance of your main window and pass it here if needed
    editor = ColorEditorApp(None, ["path_to_your_image1.jpg", "path_to_your_image2.jpg"])  # Replace with actual image paths
    editor.show()
    sys.exit(app.exec_())



# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QGridLayout, QSizePolicy, QSlider, QHBoxLayout, QPushButton, QMainWindow, QApplication
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPixmap
# from PIL import Image, ImageEnhance
# import io
# import os
# import sys

# class ColorEditorApp(QMainWindow):
#     def __init__(self, image_paths):
#         super().__init__()

#         self.setWindowTitle("Image Color Editor")
#         self.setGeometry(300, 300, 1200, 800)

#         # Main layout with a scroll area
#         self.central_widget = QWidget(self)
#         self.main_layout = QVBoxLayout(self.central_widget)
#         self.setCentralWidget(self.central_widget)

#         # Create a scroll area
#         self.scroll_area = QScrollArea(self)
#         self.scroll_area.setWidgetResizable(True)

#         # Create a container widget to hold the grid layout
#         self.container_widget = QWidget()
#         self.grid_layout = QGridLayout(self.container_widget)

#         # Add container widget to scroll area
#         self.scroll_area.setWidget(self.container_widget)
#         self.main_layout.addWidget(self.scroll_area)

#         # Create sliders layout
#         self.controls_layout = QVBoxLayout()

#         # Display all the selected images in a grid layout
#         self.display_images(image_paths)

#         # Create image controls for sliders
#         self.create_controls()

#     def display_images(self, image_paths):
#         """Display all selected images in a grid layout."""
#         row, col = 0, 0
#         max_columns = 3
#         self.image_labels = []
#         self.original_images = []
#         self.current_images = []

#         for image_path in image_paths:
#             if not os.path.exists(image_path):
#                 continue

#             # Load and store the original image
#             original_image = Image.open(image_path)
#             self.original_images.append(original_image)
#             self.current_images.append(original_image.copy())

#             # Create a QLabel to display the image
#             image_label = QLabel(self)
#             pixmap = self.image_to_pixmap(original_image)
#             image_label.setPixmap(pixmap.scaled(200, 200, aspectRatioMode=1))
#             image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#             self.grid_layout.addWidget(image_label, row, col)
#             self.image_labels.append(image_label)

#             # Update grid placement
#             col += 1
#             if col >= max_columns:
#                 col = 0
#                 row += 1

#     def image_to_pixmap(self, image):
#         """Convert a PIL image to QPixmap."""
#         image = image.convert("RGBA")
#         byte_array = io.BytesIO()
#         image.save(byte_array, format='PNG')
#         byte_array.seek(0)
#         pixmap = QPixmap()
#         pixmap.loadFromData(byte_array.getvalue())
#         return pixmap

#     def create_controls(self):
#         """Create control buttons and sliders for image editing."""
#         slider_layout = QVBoxLayout()

#         # Brightness slider
#         self.brightness_slider = self.create_slider("Brightness", slider_layout, self.update_image)
#         self.contrast_slider = self.create_slider("Contrast", slider_layout, self.update_image)
#         self.saturation_slider = self.create_slider("Saturation", slider_layout, self.update_image)
#         self.sharpness_slider = self.create_slider("Sharpness", slider_layout, self.update_image)

#         self.main_layout.addLayout(slider_layout)

#     def create_slider(self, name, layout, callback):
#         """Create a slider with labels and connect it to a callback."""
#         slider = QSlider(Qt.Horizontal)
#         slider.setRange(0, 200)
#         slider.setValue(100)
#         slider.valueChanged.connect(callback)

#         label = QLabel(f"{name}: 100")
#         slider.valueChanged.connect(lambda value: label.setText(f"{name}: {value}"))

#         layout.addWidget(slider)
#         layout.addWidget(label)
#         return slider

#     def update_image(self):
#         """Update all displayed images based on the slider values."""
#         brightness_value = self.brightness_slider.value() / 100.0
#         contrast_value = self.contrast_slider.value() / 100.0
#         saturation_value = self.saturation_slider.value() / 100.0
#         sharpness_value = self.sharpness_slider.value() / 100.0

#         for idx, original_image in enumerate(self.original_images):
#             image = ImageEnhance.Brightness(original_image).enhance(brightness_value)
#             image = ImageEnhance.Contrast(image).enhance(contrast_value)
#             image = ImageEnhance.Color(image).enhance(saturation_value)
#             image = ImageEnhance.Sharpness(image).enhance(sharpness_value)
#             self.current_images[idx] = image

#             pixmap = self.image_to_pixmap(image)
#             self.image_labels[idx].setPixmap(pixmap.scaled(200, 200, aspectRatioMode=1))

# # Main function to run the application
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     editor = ColorEditorApp(["path_to_your_image1.jpg", "path_to_your_image2.jpg"])  # Replace with actual image paths
#     editor.show()
#     sys.exit(app.exec_())


