from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance
import sys
import io

class ImageEditorApp(QMainWindow):
    image_saved = pyqtSignal(str)  # Signal to emit the saved image path

    def __init__(self, image_path):
        super().__init__()
        self.load_styles("styles.qss") 
        # Set up the main window
        self.setWindowTitle("MV | Printing Software")
        self.setGeometry(100, 100, 800, 600)

        # Store the image path for saving purposes
        self.image_path = image_path

        # Create a central widget and a horizontal layout
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)  # Use QHBoxLayout for side-by-side arrangement

        # Create a vertical layout for the controls
        self.controls_layout = QVBoxLayout()

        self.create_controls()
        
        # Add controls layout to the main layout
        self.main_layout.addLayout(self.controls_layout)

        # Create a label to display the image
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(500, 500)  # Set a standard size for the displayed image
        self.main_layout.addWidget(self.image_label)

        # Load and display the image
        self.original_image = Image.open(image_path)
        self.image = self.original_image.copy()
        self.display_image()

        self.setCentralWidget(self.central_widget)

    def load_styles(self, filename):
        """Load styles from a QSS file and apply them to the application."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

    def display_image(self):
        """Display the image in the label."""
        pixmap = self.image_to_pixmap(self.image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def image_to_pixmap(self, image):
        """Convert a PIL image to QPixmap."""
        image = image.convert("RGBA")  # Ensure the image is in RGBA mode
        byte_array = io.BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array.getvalue())
        return pixmap
    def adjust_slider_value(self, slider, adjustment):
     """Adjust the slider value by a specified amount."""
     current_value = slider.value()
     new_value = current_value + adjustment
    
    # Ensure the new value is within the range
     if 0 <= new_value <= 200:
        slider.setValue(new_value)  # Update the slider value

    def create_controls(self):
        """Create control buttons and sliders for image editing."""
        # Slider layout
        slider_layout = QVBoxLayout()  # Change to QVBoxLayout for vertical arrangement of sliders
        
        # Brightness slider
        
        self.brightness_slider = QSlider()
        self.brightness_slider.setOrientation(Qt.Horizontal)
          # Horizontal
        self.brightness_slider.setRange(0, 200)
        self.brightness_slider.setValue(100)  # Start with normal brightness
        self.brightness_slider.valueChanged.connect(self.update_image)
        self.brightness_slider.valueChanged.connect(lambda value: self.update_slider_label(self.brightness_label, "Brightness", value))
        self.brightness_label = QLabel("Brightness: 100")
        self.brightness_decrease_button = QPushButton("-")
        self.brightness_decrease_button.setFixedSize(30, 30)
        self.brightness_decrease_button.clicked.connect(lambda: self.adjust_slider_value(self.brightness_slider, -10))
        self.brightness_increase_button = QPushButton("+")
        self.brightness_increase_button.setFixedSize(30, 30)
        self.brightness_increase_button.clicked.connect(lambda: self.adjust_slider_value(self.brightness_slider, 10))
        slider_layout.addWidget(self.brightness_slider)
        slider_layout.addWidget(self.brightness_decrease_button)
        slider_layout.addWidget(self.brightness_increase_button)
        slider_layout.addWidget(self.brightness_label) 
        
        
        
        

        # Contrast slider
        self.contrast_slider = QSlider()
        self.contrast_slider.setOrientation(Qt.Horizontal)  # Horizontal
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)  # Start with normal contrast
        self.contrast_slider.valueChanged.connect(self.update_image)
        self.contrast_slider.valueChanged.connect(lambda value: self.update_slider_label(self.contrast_label, "Contrast", value))
        self.contrast_label = QLabel("Contrast: 100")
        slider_layout.addWidget(self.contrast_slider)
        slider_layout.addWidget(self.contrast_label) 

          # Label to show current contrast
        
    
       
        # Saturation slider
        self.saturation_slider = QSlider()
        self.saturation_slider.setOrientation(Qt.Horizontal)  # Horizontal
        self.saturation_slider.setRange(0, 200)
        self.saturation_slider.setValue(100)  # Start with normal saturation
        self.saturation_slider.valueChanged.connect(self.update_image)
        self.saturation_slider.valueChanged.connect(lambda value: self.update_slider_label(self.saturation_label, "Saturation", value))
        self.saturation_label = QLabel("Saturation: 100")
        slider_layout.addWidget(self.saturation_slider)
        slider_layout.addWidget(self.saturation_label) 
       
        
       

        # Sharpness slider
        self.sharpness_slider = QSlider()
        self.sharpness_slider.setOrientation(Qt.Horizontal)  # Horizontal
        self.sharpness_slider.setRange(0, 200)
        self.sharpness_slider.setValue(100)  # Start with normal sharpness
        self.sharpness_slider.valueChanged.connect(self.update_image)
        self.sharpness_slider.valueChanged.connect(lambda value: self.update_slider_label(self.sharpness_label, "Sharpness", value))
        self.sharpness_label = QLabel("Sharpness: 100") 
        slider_layout.addWidget(self.sharpness_slider)
        slider_layout.addWidget(self.sharpness_label)
    
         # Label to show current sharpness
       
       
      
         # Add label below the slider

    # Add sliders to the controls layout
    

        # Add sliders to the controls layout
        self.controls_layout.addLayout(slider_layout)

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

        # Add buttons to the controls layout
        self.controls_layout.addWidget(self.rotate_left_button)
        self.controls_layout.addWidget(self.rotate_right_button)
        self.controls_layout.addWidget(self.fit_in_button)
        self.controls_layout.addWidget(self.fit_out_button)
        self.controls_layout.addWidget(self.apply_button)
    def update_slider_label(self, label, parameter_name, value):
     """Update the text of the slider's label."""
     label.setText(f"{parameter_name}: {value}")
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
        """Crop the image to fit within the display area, reducing its size."""
        target_width = 600  # Standard width for display
        target_height = 400  # Standard height for display
    
        original_width, original_height = self.image.size

        # Calculate aspect ratios
        original_aspect = original_width / original_height
        target_aspect = target_width / target_height

        if original_aspect > target_aspect:
            # Image is wider than target, crop the width
            new_height = target_height
            new_width = int(new_height * original_aspect)
        else:
            # Image is taller than target, crop the height
            new_width = target_width
            new_height = int(new_width / original_aspect)

        # Resize image to new dimensions
        self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Center crop to target dimensions
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = (new_width + target_width) // 2
        bottom = (new_height + target_height) // 2

        self.image = self.image.crop((left, top, right, bottom))
        self.display_image()  # Update the displayed image

    def fit_out(self):
        """Crop the image to fill the display area, increasing its size."""
        target_width = 600  # Standard width for display
        target_height = 400  # Standard height for display
    
        original_width, original_height = self.image.size

        # Calculate aspect ratios
        original_aspect = original_width / original_height
        target_aspect = target_width / target_height

        if original_aspect > target_aspect:
            # Image is wider than target, crop the height
            new_width = target_width
            new_height = int(new_width / original_aspect)
        else:
            # Image is taller than target, crop the width
            new_height = target_height
            new_width = int(new_height * original_aspect)

        # Resize image to new dimensions
        self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Center crop to target dimensions
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = (new_width + target_width) // 2
        bottom = (new_height + target_height) // 2

        self.image = self.image.crop((left, top, right, bottom))
        self.display_image()  # Update the displayed image

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
