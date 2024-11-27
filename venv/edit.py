from PyQt5.QtWidgets import QMainWindow,QComboBox, QLabel, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageEnhance
import sys
from PyQt5.QtCore import pyqtSignal, Qt, QRect, QSize
import io
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QImage, QPainter
class ImageEditorApp(QMainWindow):
    image_saved = pyqtSignal(str)  

    def __init__(self, image_path):
        super().__init__()
        self.load_styles("styles.qss") 
        
        self.setWindowTitle("MV | Printing Software")
        self.setGeometry(100, 100, 800, 600)

        
        self.image_path = image_path
        self.print_button = QPushButton("Print Image")
        self.print_button.clicked.connect(self.print_image)
       
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)  
       
        self.controls_layout = QVBoxLayout()

        self.create_controls()
        
       
        self.main_layout.addLayout(self.controls_layout)

       
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(500, 500) 
        self.main_layout.addWidget(self.image_label)

        
        self.original_image = Image.open(image_path)
        self.image = self.original_image.copy()
        self.original_aspect = self.original_image.width / self.original_image.height
        self.display_image()
        self.controls_layout.addWidget(self.print_button)
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
        image = image.convert("RGBA")  
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
    
    
     if 0 <= new_value <= 200:
        slider.setValue(new_value)  

    def create_controls(self):
        """Create control buttons and sliders for image editing."""
        
        slider_layout = QVBoxLayout()  
        
        

        # Add buttons to select crop size
        self.crop_size_combo = QComboBox()
        self.crop_size_combo.addItem("200x200")
        self.crop_size_combo.addItem("400x400")
        self.crop_size_combo.addItem("600x600")
        self.crop_size_combo.currentIndexChanged.connect(self.on_crop_size_change)

        self.controls_layout.addWidget(self.crop_size_combo)

        self.controls_layout.addWidget(self.print_button)
       
        

        self.brightness = QSlider()
        self.brightness.setOrientation(Qt.Horizontal)  
        self.brightness.setRange(0, 200)
        self.brightness.setValue(100)  
        self.brightness.valueChanged.connect(self.update_image)
        self.brightness.valueChanged.connect(lambda value: self.update_slider_label(self.contrast_label, "Contrast", value))
        self.br_label = QLabel("Brightness: 100")
        slider_layout.addWidget(self.brightness)
        slider_layout.addWidget(self.br_label) 
        
        
        

        
        self.contrast_slider = QSlider()
        self.contrast_slider.setOrientation(Qt.Horizontal)  
        self.contrast_slider.setRange(0, 200)
        self.contrast_slider.setValue(100)  
        self.contrast_slider.valueChanged.connect(self.update_image)
        self.contrast_slider.valueChanged.connect(lambda value: self.update_slider_label(self.contrast_label, "Contrast", value))
        self.contrast_label = QLabel("Contrast: 100")
        slider_layout.addWidget(self.contrast_slider)
        slider_layout.addWidget(self.contrast_label) 

          
        
    
       
        
        self.saturation_slider = QSlider()
        self.saturation_slider.setOrientation(Qt.Horizontal)  
        self.saturation_slider.setRange(0, 200)
        self.saturation_slider.setValue(100)  
        self.saturation_slider.valueChanged.connect(self.update_image)
        self.saturation_slider.valueChanged.connect(lambda value: self.update_slider_label(self.saturation_label, "Saturation", value))
        self.saturation_label = QLabel("Saturation: 100")
        slider_layout.addWidget(self.saturation_slider)
        slider_layout.addWidget(self.saturation_label) 
       
        
       


        self.sharpness_slider = QSlider()
        self.sharpness_slider.setOrientation(Qt.Horizontal)  
        self.sharpness_slider.setRange(0, 200)
        self.sharpness_slider.setValue(100)  
        self.sharpness_slider.valueChanged.connect(self.update_image)
        self.sharpness_slider.valueChanged.connect(lambda value: self.update_slider_label(self.sharpness_label, "Sharpness", value))
        self.sharpness_label = QLabel("Sharpness: 100") 
        slider_layout.addWidget(self.sharpness_slider)
        slider_layout.addWidget(self.sharpness_label)
    
        self.controls_layout.addLayout(slider_layout)

        
        self.rotate_left_button = QPushButton("Rotate Left")
        self.rotate_left_button.clicked.connect(self.rotate_left)

        self.rotate_right_button = QPushButton("Rotate Right")
        self.rotate_right_button.clicked.connect(self.rotate_right)

        
        self.fit_in_button = QPushButton("Fit In")
        self.fit_in_button.clicked.connect(self.fit_in)

        self.fit_out_button = QPushButton("Fit Out")
        self.fit_out_button.clicked.connect(self.fit_out)

    
        self.apply_button = QPushButton("Apply Changes")
        self.apply_button.clicked.connect(self.apply_changes)

        
        self.controls_layout.addWidget(self.rotate_left_button)
        self.controls_layout.addWidget(self.rotate_right_button)
        self.controls_layout.addWidget(self.fit_in_button)
        self.controls_layout.addWidget(self.fit_out_button)
        self.controls_layout.addWidget(self.apply_button)
        self.start_pos = None
        self.crop_size = QSize(200, 200)  # Default crop size (e.g., 200x200)
        self.crop_rect = QRect(0, 0, self.crop_size.width(), self.crop_size.height())

        # Flag to check if the user is cropping
        self.is_cropping = False
    def update_slider_label(self, label, parameter_name, value):
     """Update the text of the slider's label."""
     label.setText(f"{parameter_name}: {value}")
    def on_crop_size_change(self):
        """Change the crop size based on the selected value from the combo box."""
        selected_size = self.crop_size_combo.currentText()
        if selected_size == "200x200":
            self.crop_size = QSize(200, 200)
        elif selected_size == "400x400":
            self.crop_size = QSize(400, 400)
        elif selected_size == "600x600":
            self.crop_size = QSize(600, 600)

        # Reset the crop rectangle to the new size
        self.crop_rect = QRect(self.crop_rect.topLeft(), self.crop_size)
        self.is_cropping = False
        self.display_image()
    def mousePressEvent(self, event):
     """Start cropping when the user clicks on the image."""
     if event.button() == Qt.LeftButton:
        self.start_pos = event.pos()
        self.crop_rect.setTopLeft(self.start_pos)
        self.is_cropping = True

    def mouseMoveEvent(self, event):
     """Update the crop rectangle as the user drags the mouse."""
     if self.is_cropping and self.start_pos:
        end_pos = event.pos()
        self.crop_rect.setBottomRight(end_pos)
        self.display_image()

    def mouseReleaseEvent(self, event):
     """Finalize the cropping when the user releases the mouse."""
     if self.is_cropping:
        self.is_cropping = False
        self.apply_crop()  # Apply the crop to the image after the release

    def apply_crop(self):
        """Crop the image based on the selected area."""
        if self.crop_rect.width() > 0 and self.crop_rect.height() > 0:
            # Crop the image using the selected rectangle
            left = self.crop_rect.left()
            top = self.crop_rect.top()
            right = self.crop_rect.right()
            bottom = self.crop_rect.bottom()

            self.image = self.image.crop((left, top, right, bottom))
            self.display_image()

    
    def update_image(self):
        """Update the image based on the current slider values."""
        brightness_value = self.brightness.value() / 100.0
        contrast_value = self.contrast_slider.value() / 100.0
        saturation_value = self.saturation_slider.value() / 100.0
        sharpness_value = self.sharpness_slider.value() / 100.0

        
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
        """Fit the image inside the display area, scaling it down if necessary."""
        target_width = 600  
        target_height = 400  
        original_width, original_height = self.image.size

        original_aspect = original_width / original_height
        target_aspect = target_width / target_height

        if original_aspect > target_aspect:
            new_height = target_height
            new_width = int(new_height * original_aspect)
        else:
            new_width = target_width
            new_height = int(new_width / original_aspect)

        # Resize image to fit while maintaining aspect ratio
        self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Center crop to fit target size
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = (new_width + target_width) // 2
        bottom = (new_height + target_height) // 2

        self.image = self.image.crop((left, top, right, bottom))
        self.display_image() 
    def fit_out(self):
        """Scale up the image to fill the display area, possibly cropping if needed."""
        target_width = 600  
        target_height = 400  
        original_width, original_height = self.image.size

        original_aspect = original_width / original_height
        target_aspect = target_width / target_height

        if original_aspect > target_aspect:
            new_width = target_width
            new_height = int(new_width / original_aspect)
        else:
            new_height = target_height
            new_width = int(new_height * original_aspect)

        # Resize image to fill the target area
        self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        # Center crop to fit target size
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = (new_width + target_width) // 2
        bottom = (new_height + target_height) // 2

        self.image = self.image.crop((left, top, right, bottom))
        self.display_image()  
    def apply_changes(self):
        """Save the modified image, emit the signal, and close the window."""
        self.image.save(self.image_path)  
        self.image_saved.emit(self.image_path)  
        self.close()  
    def print_image(self):
     """Print the currently displayed image."""
     printer = QPrinter(QPrinter.HighResolution)
     print_dialog = QPrintDialog(printer, self)

     if print_dialog.exec_() == QPrintDialog.Accepted:
        
        byte_array = io.BytesIO()
        self.image.save(byte_array, format='PNG')  
        byte_array.seek(0)
        qimage = QImage()
        qimage.loadFromData(byte_array.getvalue())

        
        painter = QPainter(printer)
        if not painter.begin(printer):
            print("Failed to start painting!")
            return

        
        rect = painter.viewport()
        image_size = qimage.size()  
        scaled_size = image_size.scaled(rect.size(), Qt.KeepAspectRatio)  

        
        x_offset = (rect.width() - scaled_size.width()) // 2
        y_offset = (rect.height() - scaled_size.height()) // 2
        painter.setViewport(x_offset, y_offset, scaled_size.width(), scaled_size.height())
        painter.setWindow(qimage.rect())
        painter.drawImage(0, 0, qimage)
        painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = ImageEditorApp("path_to_your_image.jpg")  
    editor.image_saved.connect(lambda path: print(f"Image saved at {path}"))  
    editor.show()
    sys.exit(app.exec_())
