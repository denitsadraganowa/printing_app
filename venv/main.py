

from PyQt5.QtWidgets import QApplication, QDialog,QMainWindow, QSpacerItem, QFileDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout, QWidget, QScrollArea, QSizePolicy, QFrame, QCheckBox  # Added QCheckBox
from PyQt5.QtGui import QPixmap, QImage, QColor, QPainter
from PyQt5.QtCore import Qt, QSize
from color_profile_dialog import ColorProfileDialog
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import os
from print import PrintWindow
import sys
from edit import ImageEditorApp  
from PyQt5.QtGui import QPixmap, QIcon 
from color import ColorEditorApp 
import sqlite3

class ImageGridApp(QMainWindow):
    def __init__(self, collection_data=None, collection_id=None):
        super().__init__()
        self.setGeometry(100, 100, 1000, 800)
        self.image_paths = []
        self.image_widgets = [] 
        self.collection_data = collection_data  
        self.collection_id = collection_id
        self.selected_images = []
        self.image_favorites = []
        self.setWindowTitle("MV | Printing Software")
        self.resize(1200, 800)  
        self.center()
        self.db_connection = sqlite3.connect('my_database.db')  
        self.cursor = self.db_connection.cursor()
        self.print_button = QPushButton("Print All")
        self.print_button.clicked.connect(self.print_selected_images)  # Connect the button to the print function

        

        
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        top_layout = QHBoxLayout()
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        
        self.upload_button = QPushButton("Upload")
        top_layout.addWidget(self.print_button)
        self.upload_button.clicked.connect(self.import_images)
        self.color_profile_button = QPushButton("Color Profile")
        self.color_profile_button.clicked.connect(self.open_color_profile_dialog)
        top_layout.addWidget(self.color_profile_button)

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

        self.apply_stylesheet()
        if collection_data:
            self.load_collection_images(collection_data)
    def closeEvent(self, event):
        """Ensure the database connection is closed properly."""
        self.db_connection.close()
        super().closeEvent(event)


    def print_selected_images(self):
     """Print all selected images."""
     if not self.selected_images:
        print("No images selected for printing.")
        return

    # Open the print dialog to select printer
     printer = QPrinter(QPrinter.HighResolution)
     print_dialog = QPrintDialog(printer, self)
     if print_dialog.exec_() != QPrintDialog.Accepted:
        return  # If the user cancels, return

     painter = QPainter(printer)
     painter.begin(printer)

    # Set up the page layout and margin
     page_width = printer.pageRect().width()
     page_height = printer.pageRect().height()
     margin = 10  # Margin around the image on the page

    # Loop through selected images and print them one by one
     for image_path in self.selected_images:
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
            continue

        # Scale the image to fit the page while maintaining aspect ratio
        pixmap = pixmap.scaled(page_width - 2 * margin, page_height - 2 * margin, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Center the image on the page
        x_offset = (page_width - pixmap.width()) // 2
        y_offset = (page_height - pixmap.height()) // 2

        # Draw the image onto the printer
        painter.drawPixmap(x_offset, y_offset, pixmap)

        # Start a new page for the next image
        printer.newPage()

     painter.end()
     print("Printing complete.")

    def show_collection_dialog(self):
        """Show the collection in a dialog."""
        collection_names = [image_data['path'] for image_data in self.collection_data]
        collection_list = '\n'.join(collection_names)
        
        # Create a new dialog to display the collection
        dialog = QDialog(self)
        dialog.setWindowTitle("Collection Data")
        dialog.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout(dialog)
        label = QLabel(collection_list, dialog)
        layout.addWidget(label)
        
        dialog.exec_()
    def center(self):
        qr = self.frameGeometry() 
        cp = QApplication.desktop().availableGeometry().center()  
        qr.moveCenter(cp) 
        self.move(qr.topLeft()) 

    def open_color_profile_dialog(self):
     dialog = ColorProfileDialog(self)
     if dialog.exec_():
        selected_profile = dialog.profile_combo.currentText()
        
        # Depending on the profile, load the corresponding ICC profile
        input_profile = "sRGB.icc"  # Example input profile
        if selected_profile == "Adobe RGB":
            output_profile = "AdobeRGB.icc"
        elif selected_profile == "DCI-P3":
            output_profile = "DCIP3.icc"
        
        
        
        for image_container in self.image_widgets:
            image_label = image_container.findChild(QLabel)
            pixmap = image_label.pixmap()
            if pixmap:
                
                pixmap.toImage().save("temp_image.jpg")
                apply_color_profile("temp_image.jpg", input_profile, output_profile)

    
   
    def open_new_file(self, image_path):
     """Open the image editor with the selected image path."""
     self.image_editor = ImageEditorApp(image_path)  
     self.image_editor.show()
    def load_styles(self, filename):
        """Load styles from a QSS file and apply them to the application."""
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())
    def save_image_paths(self):
     """Save image metadata to the database."""
     for file_path in self.image_paths:
        file_name = os.path.basename(file_path)
        try:
            self.cursor.execute("""
                INSERT INTO Images (CollectionID, ImagePath)
                VALUES (?, ?)
            """, (self.collection_id, file_name))
            print(self.collection_id)
            self.db_connection.commit()
            print(f"Image saved to database: {file_path}")
        except sqlite3.Error as e:
            print(f"Error saving image to database: {e}")
    def load_collection_images(self, collection_data):
      """Load the images for the given collection data."""
      self.clear_layout()  
      self.image_widgets = []  

      print("Collection data:", collection_data)

      for image_data in collection_data:
        image_path = image_data['path']
        
        print(f"Processing image at path: {image_path}")

        
        image_container = self.create_image_container(image_path)
        if image_container:
            self.image_widgets.append(image_container)

      self.arrange_images_in_grid()
    def apply_color_profile(self, brightness, contrast, tint):
    
      for container in self.image_widgets:
        image_label = container.findChild(QLabel)
        pixmap = QPixmap(image_label.pixmap())  # Get the current pixmap

        if pixmap.isNull():
            continue

        image = pixmap.toImage()
        for x in range(image.width()):
            for y in range(image.height()):
                color = QColor(image.pixel(x, y))

                
                color = QColor(
                    max(0, min(255, color.red() + brightness)),
                    max(0, min(255, color.green() + brightness)),
                    max(0, min(255, color.blue() + brightness))
                )

               
                color = QColor(
                    max(0, min(255, color.red() + tint)),
                    max(0, min(255, color.green() + tint // 2)),
                    max(0, min(255, color.blue() - tint))
                )

                image.setPixel(x, y, color.rgb())

        new_pixmap = QPixmap.fromImage(image)
        image_label.setPixmap(new_pixmap)



    def apply_stylesheet(self):
        """Apply consistent stylesheet across the app."""
        self.setStyleSheet("""
            QWidget {
                background-color: #2c577a;
            }
            QLabel {
                font-size: 32px;
                color: #ffffff;
            }
            QLineEdit {
                font-size: 18px;
                background-color: #2c577a;
                color: #ffffff;
                border-radius: 20px;
                padding: 10px;
            }
            QPushButton {
                font-size: 18px;
                color: #ffffff;
                background-color: #be3228;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #145050;
            }
            QPushButton:pressed {
                background-color: #0f4c5c;
            }
            QFrame {
                background-color: #E0E0E0;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            QCheckBox {
                margin: 2px;
                color: #ffffff;
            }
            QScrollArea {
                background-color: #0f4c5c;
                border: none;
            }
        """)
    def open_print_window(self):
        """Open the PrintWindow with the selected collection."""
        collection_name = self.collection_data[0]
       
        print_window = PrintWindow(collection_name)
        print_window.show()
        
        if collection_name:
            print_window = PrintWindow(collection_name)
            print_window.show()

    def import_images(self):
     """Open a file dialog to select and import multiple images."""
     image_paths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Images (*.png *.jpg *.jpeg *.bmp)")
    
     if image_paths:
        for image_path in image_paths:
            
            absolute_path = os.path.abspath(image_path)
            if absolute_path not in self.image_paths:  
                self.image_paths.append(absolute_path)
                 
                image_container = self.create_image_container(absolute_path, False)  
                self.image_widgets.append(image_container)

        self.save_image_paths() 
        self.arrange_images_in_grid()
   
    def create_image_container(self, image_path, is_edited=False):
        FRAME_WIDTH = 384  
        FRAME_HEIGHT = 400
        container = QFrame()
        container.setFixedSize(FRAME_WIDTH, FRAME_HEIGHT)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
            return None  
        
        print(f"Loading image from path: {image_path}")
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Failed to load image from path: {image_path}")
            return None  
        print(f"Successfully loaded image from: {image_path}, Size: {pixmap.size()}")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setStyleSheet("background-color: white;")  
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
        download_button.setIcon(QIcon("images/download.jpg"))
        download_button.setIconSize(QSize(40, 40))
        edit_button = QPushButton()
        edit_button.setIcon(QIcon("images/edit.jpg"))
        edit_button.setIconSize(QSize(40, 40))
        palette_button = QPushButton()
        palette_button.setIcon(QIcon("palette.jpg"))
        palette_button.setIconSize(QSize(40, 40))
        
        delete_button = QPushButton()
        delete_button.setIcon(QIcon("images/delete.png"))
        delete_button.setIconSize(QSize(40, 40))
       

     
        for btn in [download_button, edit_button, palette_button, delete_button]:
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
        
       
        download_button.clicked.connect(lambda: self.download_image(image_path))
        palette_button.clicked.connect(self.open_selected_images_in_palette)
        
        delete_button.clicked.connect(lambda: self.delete_image_container(container))
        edit_button.clicked.connect(lambda: self.open_new_file(image_path))
        button_layout.addWidget(delete_button)
        button_panel.setFixedHeight(button_size + 10)
        
        button_layout.addWidget(download_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(palette_button)
        
        button_layout.addWidget(delete_button)

        
        button_panel.setFixedHeight(button_size + 10)

        
        container_layout.addWidget(button_panel, alignment=Qt.AlignBottom)

        return container
    def toggle_favorite(self, image_path, favorite_button):
        """Toggle the favorite status of the image and update the UI accordingly."""
        current_status = self.image_favorites.get(image_path, False)
        new_status = not current_status
        self.image_favorites[image_path] = new_status 
        
       
        favorite_button.setStyleSheet("border: 2px solid red;" if new_status else "")

        self.save_image_paths()  
    def download_image(self, image_path):
     """Download the selected image to a user-specified directory."""
     if not os.path.exists(image_path):
        print(f"Error: Image file does not exist at {image_path}")
        return

    # Open a file dialog for selecting the download directory
     directory = QFileDialog.getExistingDirectory(self, "Select Download Directory")
     if not directory:
        print("Download canceled: No directory selected.")
        return  # User canceled the directory selection

    # Get the filename from the path and build the save path
     filename = os.path.basename(image_path)
     save_path = os.path.join(directory, filename)

    # Load the image as a QPixmap and save it to the specified path
     try:
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Error: Failed to load image from {image_path}")
            return

        if pixmap.save(save_path):
            print(f"Image successfully saved to: {save_path}")
        else:
            print(f"Error: Failed to save the image to {save_path}")
     except Exception as e:
        print(f"Unexpected error occurred while downloading image: {e}")

    def delete_image_container(self, container):
     """Remove the image container from the layout, delete it, and remove it from the database."""
     print("Current collection data:", self.collection_data)
    
     try:
        # Find the index of the container in the list of image widgets
        index = self.image_widgets.index(container)
        
        # Use the index to find the corresponding image path
        if index < len(self.collection_data):
            deleted_image_path = self.collection_data[index]['path']
        else:
            print("Error: Index out of bounds in collection_data.")
            return
     except ValueError:
        print("Error: Container not found in image_widgets.")
        return
     except IndexError:
        print("Error: Image path index out of bounds.")
        return

    # Remove container from the UI
     self.grid_layout.removeWidget(container)
     container.deleteLater()

    # Remove the container and path from their respective lists
     self.image_widgets.pop(index)
     self.collection_data.pop(index)

    # Delete the image record from the database
     try:
        self.cursor.execute("""
            DELETE FROM Images WHERE ImagePath = ? AND CollectionID = ?
        """, (os.path.basename(deleted_image_path), self.collection_id))
        self.db_connection.commit()
        print(f"Image deleted from database: {deleted_image_path}")
     except sqlite3.Error as e:
        print(f"Error deleting image from database: {e}")

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
     if not self.selected_images: 
        print("No images selected to open in ColorEditorApp.")
        return  
     self.color_editor = ColorEditorApp(self, self.selected_images)  
  
     self.color_editor.show()



    def clear_layout(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.image_widgets.clear()
    def create_new_collection(self):
        """Handle the creation of a new collection."""
        collection_name, ok = QInputDialog.getText(self, "New Collection", "Enter collection name:")
        if ok and collection_name:
            
            self.collection_data = []  
            print(f"New collection created: {collection_name}")
            
           
            self.load_collection_images(self.collection_data)  

    def arrange_images_in_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        num_columns = 3  
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
    
    
    def refresh_images(self, image_paths):
        """Refresh the displayed images in the main window."""
        self.image_paths = image_paths 
        self.display_images(self.image_paths)  

    def display_images(self, image_paths):
        """Display images in the main window."""
        
        for label in self.image_labels:
            label.deleteLater()  
        self.image_labels.clear()  

        row, col = 0, 0
        max_columns = 3
        self.grid_layout = QGridLayout() 
        self.container_widget.setLayout(self.grid_layout)  

        for image_path in image_paths:
            if not os.path.exists(image_path):
                continue
            
           
            image_label = QLabel(self)
            pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio)
            image_label.setPixmap(pixmap)
            image_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.grid_layout.addWidget(image_label, row, col)
            self.image_labels.append(image_label)

            
            col += 1
            if col >= max_columns:
                col = 0
                row += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageGridApp()
    window.show()
    sys.exit(app.exec_())
