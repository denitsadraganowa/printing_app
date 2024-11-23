import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QComboBox, QMessageBox
from PyQt5.QtGui import QImage, QPainter, QPixmap
from PyQt5.QtPrintSupport import QPrinter,QPrinterInfo, QPrintDialog
from PyQt5.QtCore import Qt

class PrintWindow(QWidget):
    def __init__(self, images):
        super().__init__()
        self.setWindowTitle("Print  - MV Printing Software")
        self.setGeometry(100, 100, 800, 600)

        self.images = images  # List of image paths to print

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title label
        title = QLabel("Upload and Print Image")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Button to print the collection
        self.print_button = QPushButton("Print Collection", self)
        self.print_button.clicked.connect(self.print_collection)
        layout.addWidget(self.print_button)

        # ComboBox to select printer
        self.printer_label = QLabel("Select Printer:")
        self.printer_combo = QComboBox(self)
        self.load_printers()
        layout.addWidget(self.printer_label)
        layout.addWidget(self.printer_combo)

        self.setLayout(layout)

    def load_printers(self):
        """Load available printers into the ComboBox."""
        printers = QPrinterInfo.availablePrinters()
        for printer in printers:
            self.printer_combo.addItem(printer.printerName())

    def print_collection(self):
        """Print all images in the collection."""
        if not self.images:
            self.show_error("No images to print", "Please select a collection with images to print.")
            return

        # Get the selected printer
        printer_name = self.printer_combo.currentText()
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPrinterName(printer_name)

        # Open a print dialog to allow user to select options
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Print each image in the collection
            for image_path in self.images:
                self.perform_printing(printer, image_path)

    def perform_printing(self, printer, image_path):
        """Perform the actual printing of the image."""
        image = QImage(image_path)
        if image.isNull():
            self.show_error("Invalid image", f"Failed to load the image: {image_path}")
            return

        painter = QPainter(printer)
        painter.begin(printer)
        rect = painter.viewport()
        image = image.scaled(rect.size(), Qt.KeepAspectRatio)
        painter.drawImage(0, 0, image)
        painter.end()

    def show_error(self, title, message):
        """Show error message."""
        QMessageBox.critical(self, title, message)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = PrintWindow([])  # Empty list for testing
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")

