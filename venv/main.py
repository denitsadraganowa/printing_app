

from PyQt5.QtWidgets import QApplication, QMainWindow, QSpacerItem, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QWidget, QScrollArea, QSizePolicy, QFrame, QCheckBox  # Added QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt5.QtCore import Qt, QSize
import os

import sys
from edit import ImageEditorApp  
from PyQt5.QtGui import QPixmap, QIcon 
from color import ColorEditorApp 


class ImageGridApp(QMainWindow):
    def __init__(self, collection_data=None):
        super().__init__()

        self.image_paths = []
        self.image_widgets = [] 
        self.collection_data = collection_data 
        self.selected_images = []
        self.image_favorites=[]
        self.setWindowTitle("MV | Printing Software")
        self.resize(1200, 800)  
        self.center()
        self.load_styles("main.qss")
        
       
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

 
        top_layout = QHBoxLayout()
        
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_layout.addItem(spacer)

       
        self.upload_button = QPushButton(self)
        self.upload_button.setIcon(QIcon("upload.jpg"))
        self.upload_button.clicked.connect(self.import_images)

        
        top_layout.addWidget(self.upload_button)

       
        self.main_layout.addLayout(top_layout)

  
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.grid_layout = QGridLayout(self.image_container)  

    
        self.scroll_area.setWidget(self.image_container)
        self.main_layout.addWidget(self.scroll_area)

      
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

       
        if collection_data:
            self.load_collection_images(collection_data)

    def load_collection_images(self, collection_data):
     """Load the images for the given collection data."""
     self.clear_layout()  
     self.image_widgets = []  # Reset the list of image containers

     print("Collection data:", collection_data)

     for image_data in collection_data:
        image_path = image_data['path']
        is_favorite = image_data['edited']
        print(f"Processing image at path: {image_path}, Favorite: {is_favorite}")

        # Create and append image containers
        image_container = self.create_image_container(image_path, is_favorite)
        if image_container:
            self.image_widgets.append(image_container)

     self.arrange_images_in_grid()


    
  


    
    def center(self):
        """Center the window on the screen."""
        qr = self.frameGeometry() 
        cp = QApplication.desktop().availableGeometry().center()  
        qr.moveCenter(cp) 
        self.move(qr.topLeft()) 
    
    def open_new_file(self, image_path):
     """Open the image editor with the selected image path."""
     self.image_editor = ImageEditorApp(image_path)  
     self.image_editor.show()
    def load_styles(self, filename):
        """Load styles from a QSS file and apply them to the application."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())
    def save_image_paths(self):
     """Save the list of image paths and their favorite status to a file."""
     with open("images.txt", "w") as file:
        for collection_name, images in self.image_collections.items():
            file.write(f"{collection_name}\n")  
            for path, is_favorite in images:
                file.write(f"{path},{is_favorite}\n") 

    def import_images(self):
     """Open a file dialog to select and import multiple images."""
     image_paths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Images (*.png *.jpg *.jpeg *.bmp)")
    
     if image_paths:
        for image_path in image_paths:
            
            absolute_path = os.path.abspath(image_path)
            if absolute_path not in self.image_paths:  
                self.image_paths.append(absolute_path)
                self.image_favorites[absolute_path] = False  
                image_container = self.create_image_container(absolute_path, False)  
                self.image_widgets.append(image_container)

        self.save_image_paths() 
        self.arrange_images_in_grid()
   
    def create_image_container(self, image_path, is_edited=False):
        FRAME_WIDTH = 384   
        FRAME_HEIGHT = 576 
        container = QFrame()
        container.setFixedSize(FRAME_WIDTH, FRAME_HEIGHT)
        container.setFrameShape(QFrame.Box)
        container.setStyleSheet("""
        QFrame {
            background-color: #E0E0E0; 
            border-radius: 0px; 
            padding: 0px;
            margin: 0px;
        }
    """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        image_label = QLabel(self)
        pixmap = QPixmap(image_path)
        if not os.path.exists(image_path):
            print(f"Error: Image file does not exist at {image_path}")
            return None  # Skip if image doesn't exist
        
        print(f"Loading image from path: {image_path}")
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Failed to load image from path: {image_path}")
            return None  # If image fails to load, return None
        
        print(f"Successfully loaded image from: {image_path}, Size: {pixmap.size()}")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background-color: white;")  # Background to show framing area
        container_layout.addWidget(image_label)


        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background-color: white;") 
        container_layout.addWidget(image_label)
        
        checkbox = QCheckBox(container)
        checkbox.setStyleSheet("QCheckBox { margin: 2px; }")
        checkbox.setGeometry(5, 5, 20, 20)  

        
        checkbox.toggled.connect(lambda checked, path=image_path: self.update_selected_images(checked, path))

        container_layout.addWidget(image_label)
        
        
        button_panel = QWidget()
        button_panel.setStyleSheet("background-color:#f5f5f5;")
        button_layout = QHBoxLayout(button_panel)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(0)

       
        button_size = 60

        download_button = QPushButton()
        download_button.setIcon(QIcon("download.jpg"))
        download_button.setIconSize(QSize(40, 40))
        edit_button = QPushButton()
        edit_button.setIcon(QIcon("edit.jpg"))
        edit_button.setIconSize(QSize(40, 40))
        palette_button = QPushButton()
        palette_button.setIcon(QIcon("palette.jpg"))
        palette_button.setIconSize(QSize(40, 40))
        favorite_button = QPushButton()
        favorite_button.setIcon(QIcon("heart.jpg"))
        favorite_button.setIconSize(QSize(40, 40))
        delete_button = QPushButton()
        delete_button.setIcon(QIcon("delete.png"))
        delete_button.setIconSize(QSize(40, 40))

     
        for btn in [download_button, edit_button, palette_button, favorite_button, delete_button]:
            btn.setFixedSize(button_size, button_size)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f5f5f5;
                    border: none;
                    border-radius: 5px;
                    color: white;
                    font-size: 22px;
                    padding: 0px;
                    margin: 0px;
                }
                QPushButton:hover {
                    background-color: #357ABD;
                }
            """)
        favorite_button.setStyleSheet("border: 2px solid red;" if is_edited else "")
       
        download_button.clicked.connect(lambda: self.download_image(image_path))
        palette_button.clicked.connect(self.open_selected_images_in_palette)
        favorite_button.clicked.connect(lambda: self.toggle_favorite(image_path, favorite_button))  # Connect favorite button to toggle
        delete_button.clicked.connect(lambda: self.delete_image_container(container))
        edit_button.clicked.connect(lambda: self.open_new_file(image_path))
        button_layout.addWidget(delete_button)
        button_panel.setFixedHeight(button_size + 10)
        
        button_layout.addWidget(download_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(palette_button)
        button_layout.addWidget(favorite_button)
        button_layout.addWidget(delete_button)

        # Set the height of the button panel to match the button size
        button_panel.setFixedHeight(button_size + 10)

        # Add the button panel to the container layout, attach it closely to the image
        container_layout.addWidget(button_panel, alignment=Qt.AlignBottom)

        return container
    def toggle_favorite(self, image_path, favorite_button):
        """Toggle the favorite status of the image and update the UI accordingly."""
        current_status = self.image_favorites.get(image_path, False)
        new_status = not current_status
        self.image_favorites[image_path] = new_status  # Update favorite status in the dictionary
        
        # Update button appearance based on new favorite status
        favorite_button.setStyleSheet("border: 2px solid red;" if new_status else "")

        self.save_image_paths()  # Save the updated favorite status to the file
    def download_image(self, image_path):
     """Download the selected image to a user-specified directory."""
     directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
    
     if directory:
        # Define the full path where the image will be saved
        filename = os.path.basename(image_path)  # Get the original file name
        save_path = os.path.join(directory, filename)
        
        # Save the image as a new file in the selected directory
        pixmap = QPixmap(image_path)
        pixmap.save(save_path)  # Save the image
        
        # Optionally, show a message that the download was successful
        print(f"Image saved to: {save_path}")
    def delete_image_container(self, container):
     """Remove the image container from the layout and delete it."""
    # Find the index of the container in the image_widgets list
     index = self.image_widgets.index(container)
    
    # Remove the container widget from the layout
     self.grid_layout.removeWidget(container)
     container.deleteLater()
    
    # Remove the container and path from their respective lists
     self.image_widgets.pop(index)
     deleted_image_path = self.image_paths.pop(index)
    
    # Save the updated list of paths
     self.save_image_paths()
    
    # Rearrange the remaining images in the grid
     self.arrange_images_in_grid()

    def update_selected_images(self, checked, path):
     """Update the list of selected images based on the checkbox state."""
     if checked:
        self.selected_images.append(path)
     else:
        if path in self.selected_images:
            self.selected_images.remove(path)


    def open_selected_images_in_palette(self):
     """Open ColorEditorApp with all selected images."""
     if not self.selected_images:  # Check if no images are selected
        print("No images selected to open in ColorEditorApp.")
        return  # Do nothing if no images are selected
     self.color_editor = ColorEditorApp(self, self.selected_images)  # Pass the main window instance (self) as an argument
  # Pass the list of selected image paths
     self.color_editor.show()



    def clear_layout(self):
        """Clear the current layout of image containers."""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.image_widgets.clear()

    def arrange_images_in_grid(self):
        """Arrange image containers dynamically in a grid layout."""
        # Clear existing widgets from the grid layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # Detach widget from layout but keep it in memory

        # Populate the grid layout with all image containers
        num_columns = 3  # Example column count
        row = 0
        col = 0
        for image_container in self.image_widgets:
            self.grid_layout.addWidget(image_container, row, col)
            col += 1
            if col >= num_columns:
                col = 0
                row += 1

    def fit_in(self, pixmap, target_width, target_height):
        """Resize the image to fit within the target dimensions while maintaining aspect ratio."""
        return pixmap.scaled(target_width, target_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    #### don't need the following 2 defs
    def refresh_images(self, image_paths):
        """Refresh the displayed images in the main window."""
        self.image_paths = image_paths  # Update with the new paths if needed
        self.display_images(self.image_paths)  # Reload and display images

    def display_images(self, image_paths):
        """Display images in the main window."""
        # Clear existing labels
        for label in self.image_labels:
            label.deleteLater()  # Clean up previous labels
        self.image_labels.clear()  # Clear the list of labels

        row, col = 0, 0
        max_columns = 3
        self.grid_layout = QGridLayout()  # Assuming you have a grid layout to display images
        self.container_widget.setLayout(self.grid_layout)  # Set the layout for your container

        for image_path in image_paths:
            if not os.path.exists(image_path):
                continue
            
            # Create a QLabel to display the image
            image_label = QLabel(self)
            pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.grid_layout.addWidget(image_label, row, col)
            self.image_labels.append(image_label)

            # Update grid placement
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGridApp()
    window.show()
    sys.exit(app.exec_())
