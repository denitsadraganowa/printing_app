from PyQt5.QtWidgets import QDialog, QComboBox, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow, QSpacerItem, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QWidget, QScrollArea, QSizePolicy, QFrame, QCheckBox  # Added QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPixmap, QImage
from PIL import Image, ImageCms
import io
class ColorProfileDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Color Profile")
        self.setGeometry(200, 200, 400, 300)

        # Create a combo box to choose a color profile
        self.profile_combo = QComboBox(self)
        self.profile_combo.addItem("sRGB")
        self.profile_combo.addItem("DCI-P3")
        self.profile_combo.addItem("Adobe RGB")
        self.profile_combo.addItem("ProPhoto RGB")

        # Apply button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_profile)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Choose a Color Profile"))
        layout.addWidget(self.profile_combo)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_profile(self):
        # Get the selected profile and process it
        profile = self.profile_combo.currentText()
        self.accept()  # Close the dialog
        print(f"Selected profile: {profile}")
        self.apply_color_profile(profile)
    def apply_color_profile(self, profile_name):
    
     for container in self.image_widgets:
        image_label = container.findChild(QLabel)
        pixmap = image_label.pixmap()  # Get the current pixmap

        if pixmap is None or pixmap.isNull():
            continue

        # Convert pixmap to QImage
        image = pixmap.toImage()

        # Convert the QImage to a Pillow image
        buffer = io.BytesIO()
        image.save(buffer, 'BMP')  # Save to in-memory buffer as BMP (no compression)
        buffer.seek(0)

        pil_image = Image.open(buffer)

        # Select the color profile
        input_profile = "sRGB.icc"  # Assuming the image is in sRGB, change as needed
        output_profile = self.get_output_profile(profile_name)  # Get target profile (e.g., Adobe RGB)

        # Apply color profile conversion using Pillow
        try:
            pil_image = ImageCms.profileToProfile(pil_image, input_profile, output_profile)
        except Exception as e:
            print(f"Error applying color profile: {e}")
            continue

        # Convert the Pillow image back to QImage
        pil_image = pil_image.convert('RGB')
        img_bytes = pil_image.tobytes()

        # Create a new QImage with the converted pixel data
        new_qimage = QImage(img_bytes, pil_image.width, pil_image.height, pil_image.width * 3, QImage.Format_RGB888)

        # Convert QImage back to QPixmap
        new_pixmap = QPixmap.fromImage(new_qimage)

        # Set the updated pixmap on the label
        image_label.setPixmap(new_pixmap)

     def get_output_profile(self, profile_name):
      """Return the path to the ICC profile file based on the selected profile."""
      profiles = {
        'sRGB': 'path/to/sRGB.icc',
        'DCI-P3': 'path/to/DCI-P3.icc',
        'Adobe RGB': 'path/to/AdobeRGB.icc',
        'ProPhoto RGB': 'path/to/ProPhotoRGB.icc'
    }
      return profiles.get(profile_name, 'path/to/sRGB.icc')