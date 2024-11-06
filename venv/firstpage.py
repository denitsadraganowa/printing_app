import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from main import ImageGridApp  # Assuming ImageGridApp is defined in main.py
import os

def load_collections(file_path):
    collections = []
    with open(file_path, 'r') as file:
        collection = None
        for line in file:
            line = line.strip()
            if line.startswith("Collection"):
                if collection:
                    collections.append(collection)
                collection = {"name": line, "images": []}
            elif line:
                image_path, edited = line.split(',')
                # Convert relative paths to absolute paths
                image_path = os.path.abspath(image_path.strip())  # Ensure path is correct
                edited = edited.lower() == "true"
                collection["images"].append({"path": image_path, "edited": edited})
        if collection:  # Add last collection
            collections.append(collection)
    return collections


collections = load_collections("image_collections.txt")


# Custom button for collection
class CollectionButton(QPushButton):
    def __init__(self, collection, image_collections, parent=None):
        super().__init__(collection['name'], parent)
        self.collection_name = collection['name']
        self.image_collections = image_collections  # Store the collections data

        # Display the first image in the collection
        if collection['images']:
            pixmap = QPixmap(collection['images'][0]["path"])
            self.setIcon(QIcon(pixmap))  # Set the icon using QIcon
            self.setIconSize(pixmap.rect().size())

        # Size adjustment
        self.setFixedSize(300, 300)

        self.clicked.connect(self.open_collection_screen)

    def open_collection_screen(self):
        """Open the image grid screen for the selected collection."""
        # Access collection data using the name
        collection_data = next((col for col in self.image_collections if col['name'] == self.collection_name), None)
        if collection_data:
            print(collection_data['images'])
            collection_screen = ImageGridApp(collection_data['images'])
            collection_screen.show()


# Main Window to display the collection screen and switch between screens
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MV | Printing Software")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.stacked_widget = QStackedWidget(self)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.addWidget(self.stacked_widget)

        self.init_collection_screen()

    def init_collection_screen(self):
        collection_screen = QWidget()
        layout = QVBoxLayout()

        # Add title for the collection screen
        title = QLabel("Photo Collections")
        title.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(title)

        # Create a horizontal layout for collection buttons
        row_layout = QHBoxLayout()

        # Create buttons for collections (first collection is the largest)
        for i, collection in enumerate(collections):
            collection_button = CollectionButton(collection, collections)
            row_layout.addWidget(collection_button)

        # Add a scroll area to contain the buttons
        scroll_area = QScrollArea(self)
        scroll_widget = QWidget()
        scroll_widget.setLayout(row_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

        collection_screen.setLayout(layout)

        # Add the collection screen to the stacked widget
        self.stacked_widget.addWidget(collection_screen)

    def show_collection_screen(self, collection_screen):
        self.stacked_widget.addWidget(collection_screen)
        self.stacked_widget.setCurrentWidget(collection_screen)


# Main app logic
app = QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec_())
