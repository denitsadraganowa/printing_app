from PyQt5.QtWidgets import QApplication, QMainWindow,QSpacerItem , QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QWidget, QScrollArea, QSizePolicy, QFrame
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt5.QtCore import Qt, QSize

import sys
from edit import ImageEditorApp  # Import the ImageEditorApp class from edit.py
from PyQt5.QtGui import QPixmap, QIcon 
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
     
    
     container_layout.addWidget(image_label)
    
    # Button panel
     button_panel = QWidget()
     button_panel.setStyleSheet("background-color:#f5f5f5;")  # Set background color to white
     button_layout = QHBoxLayout(button_panel)
     button_layout.setContentsMargins(0, 0, 0, 0)
     button_layout.setSpacing(0)  #  # Reduce spacing between buttons
    
    # Define button size before using it
     button_size = 60  # Increase button size to make them more proportionate

    # Create and add buttons
     download_button = QPushButton()
     download_button.setIcon(QIcon("download.jpg"))  # Set custom download icon
     download_button.setIconSize(QSize(40, 40))
     edit_button = QPushButton()
     edit_button.setIcon(QIcon("edit.jpg"))  # Set custom edit icon
     edit_button.setIconSize(QSize(40, 40))
     palette_button = QPushButton()
     palette_button.setIcon(QIcon("palette.jpg"))  # Set custom palette icon
     palette_button.setIconSize(QSize(40, 40))
     favorite_button = QPushButton()
     favorite_button.setIcon(QIcon("heart.jpg"))  # Set custom favorite icon
     favorite_button.setIconSize(QSize(40, 40))
     delete_button = QPushButton()
     delete_button.setIcon(QIcon("delete.png"))
     delete_button.setIconSize(QSize(40, 40))
    # Set button sizes and styles
     for btn in [download_button, edit_button, palette_button, favorite_button, delete_button]:
        btn.setFixedSize(button_size, button_size)
        btn.setStyleSheet("""
    QPushButton {
        background-color: #f5f5f5;  /* Button background color */
        border: none;  /* No border */
        border-radius: 5px;  /* Rounded corners */
        color: white;  /* Text color */
        font-size: 22px;  /* Font size */
        padding: 0px;  /* No padding */
        margin: 0px;  /* No margin */
              }
    QPushButton:hover {
        background-color: #357ABD;  /* Background color on hover */
            }
        """)


    # Add buttons to the horizontal layout
     button_layout.addWidget(download_button)
     button_layout.addWidget(edit_button)
     button_layout.addWidget(palette_button)
     button_layout.addWidget(favorite_button)
     button_layout.addWidget(delete_button)

    # Set the height of the button panel to match the button size
     button_panel.setFixedHeight(button_size + 10)
    
    # Add the button panel to the container layout, attach it closely to the image
     container_layout.addWidget(button_panel, alignment=Qt.AlignBottom)  # Attach button panel to the bottom of the image
    
     return container

    def fit_in(self, pixmap, target_width, target_height):
        # Scale the pixmap to fit within the target dimensions while maintaining aspect ratio
        return pixmap.scaled(target_width, target_height, aspectRatioMode=1) 

    def fit_in(self, pixmap, target_width, target_height):
        """Scale image to fit inside the target size (Fit In)."""
        return pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def fit_out(self, pixmap, target_width, target_height):
        """Scale image to fill the target size, cropping where necessary (Fit Out)."""
        return pixmap.scaled(target_width, target_height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

    def open_image_in_new_window(self, image_path):
        """Open the image in the other application window (edit.py) by passing the image path."""
        self.image_editor = ImageEditorApp(image_path)
        self.image_editor.image_saved.connect(self.update_image)
        self.image_editor.show()

    def update_image(self, image_path):
        """Update the displayed image after editing."""
        self.clear_layout()
        edited_container = self.create_image_container(image_path)
        self.image_widgets.append(edited_container)
        self.arrange_images_in_grid()

    def arrange_images_in_grid(self):
        """Arrange image containers in a responsive grid layout."""
        num_images = len(self.image_widgets)
        container_width = self.image_container.width()
        image_width = 220  # Adjust to the size of the image container + padding and margins
        columns = max(1, container_width // image_width)

        row, col = 0, 0
        for index, container in enumerate(self.image_widgets):
            self.grid_layout.addWidget(container, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def resizeEvent(self, event):
        """Override resize event to re-arrange images on window resize."""
        super().resizeEvent(event)
        self.arrange_images_in_grid()

    def clear_layout(self):
        """Clear all image widgets from the layout."""
        for widget in self.image_widgets:
            self.grid_layout.removeWidget(widget)
            widget.deleteLater()
        self.image_widgets = []

# Main function to run the application
def main():
    app = QApplication(sys.argv)
    window = ImageGridApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
