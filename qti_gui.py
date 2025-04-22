#!/usr/bin/env python3
"""
qti_gui.py

GUI interface for the QTI Converter application.
Provides a file selection dialog for selecting multiple .txt or .md files
to be converted to QTI format for Canvas LMS.
"""

import sys
import os
import cv2
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                              QVBoxLayout, QLabel, QFileDialog, QWidget,
                              QListWidget, QHBoxLayout, QFrame, QDialog,
                              QPlainTextEdit, QMessageBox)
from PySide6.QtCore import Qt
from qtiConverterApp import makeQti


class HotspotPolygonTool:
    """Implements the polygon creation tool for hotspot coordinates directly within the GUI app."""
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.points = []
        self.polygon_closed = False
        self.img = None
    
    def click_event(self, event, x, y, flags, param):
        """Mouse callback function for cv2"""
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.polygon_closed:
                return
            self.points.append((x, y))
            if len(self.points) > 1:
                cv2.line(self.img, self.points[-2], self.points[-1], (0, 255, 0), 2)
            cv2.circle(self.img, (x, y), 5, (0, 0, 255), -1)
            cv2.imshow('image', self.img)
            
        elif event == cv2.EVENT_LBUTTONDBLCLK:
            if len(self.points) > 2:
                cv2.line(self.img, self.points[-1], self.points[0], (0, 255, 0), 2)
                self.polygon_closed = True
                cv2.imshow('image', self.img)
    
    def run(self):
        """Run the hotspot polygon tool"""
        # Load the image
        self.img = cv2.imread(str(Path(self.image_path).resolve()))
        if self.img is None:
            raise ValueError("Could not open or find the image")
        
        # Display the image
        cv2.imshow('image', self.img)
        cv2.setWindowTitle('image', "Click to add points, double-click to close polygon, then press any key")
        cv2.setMouseCallback('image', self.click_event)
        
        # Wait until the user presses a key
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        # Calculate the coordinates as percentages
        height, width, _ = self.img.shape
        percent_coords = [(x / width, y / height) for x, y in self.points]
        
        return percent_coords


class CoordinatesDialog(QDialog):
    def __init__(self, coordinates, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hotspot Coordinates")
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)
        
        # Set up the layout
        layout = QVBoxLayout(self)
        
        # Add instructions
        instructions = QLabel("These coordinates can be copied and pasted into your hotspot question.")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Add text area with coordinates
        self.text_area = QPlainTextEdit()
        self.text_area.setPlainText(coordinates)
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)
        
        # Add a copy button
        copy_button = QPushButton("Copy Coordinates to Clipboard")
        copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_button)
        
        # Add a close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        # Copy the coordinates to the clipboard, excluding the first line which says "Polygon vertices"
        clipboard.setText('\n'.join(self.text_area.toPlainText().splitlines()[1:]))
        QMessageBox.information(self, "Copied", "Coordinates copied to clipboard.")


class QtiConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTI Converter")
        self.setGeometry(100, 100, 600, 400)
        
        # Initialize the last directory used (for file dialogs)
        self.last_directory = str(Path.home())
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header label
        header_label = QLabel("QTI Converter")
        header_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
        header_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header_label)
        
        # Description label
        desc_label = QLabel("Select text files to convert to QTI format for Canvas LMS")
        desc_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(desc_label)
        
        # File list widget
        self.file_list = QListWidget()
        main_layout.addWidget(self.file_list)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        # Add files button
        self.select_button = QPushButton("Select Files")
        self.select_button.setMinimumHeight(40)
        self.select_button.clicked.connect(self.select_files)
        button_layout.addWidget(self.select_button)
        
        # Convert button
        self.convert_button = QPushButton("Convert to QTI")
        self.convert_button.setMinimumHeight(40)
        self.convert_button.setEnabled(False)  # Initially disabled
        self.convert_button.clicked.connect(self.convert_files)
        button_layout.addWidget(self.convert_button)
        
        # Hotspot coordinates button
        self.hotspot_button = QPushButton("Hotspot Coordinates")
        self.hotspot_button.setMinimumHeight(40)
        self.hotspot_button.clicked.connect(self.generate_hotspot_coordinates)
        button_layout.addWidget(self.hotspot_button)
        
        main_layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFrameShape(QFrame.Panel)
        self.status_label.setFrameShadow(QFrame.Sunken)
        self.status_label.setMinimumHeight(30)
        main_layout.addWidget(self.status_label)
        
        # Store selected files
        self.selected_files = []
    
    def select_files(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Text files (*.txt *.md)")
        file_dialog.setViewMode(QFileDialog.List)
        file_dialog.setDirectory(self.last_directory)  # Use the last directory
        
        if file_dialog.exec():
            # Clear previous selections
            self.file_list.clear()
            self.selected_files = file_dialog.selectedFiles()
            
            # Add selected files to the list widget
            for file_path in self.selected_files:
                self.file_list.addItem(os.path.basename(file_path))
            
            # Enable convert button if files are selected
            self.convert_button.setEnabled(len(self.selected_files) > 0)
            self.status_label.setText(f"{len(self.selected_files)} files selected")
            
            # Remember the directory for future file dialogs
            if self.selected_files:
                self.last_directory = os.path.dirname(self.selected_files[0])
    
    def convert_files(self):
        if not self.selected_files:
            self.status_label.setText("No files selected")
            return
        
        self.status_label.setText("Converting files...")
        successful = 0
        all_errors = []
        
        # Process each selected file
        for file_path in self.selected_files:
            try:
                # Default separator is '.'
                converter = makeQti(file_path, '.')
                converter.run()
                
                # Check for errors collected during conversion
                if converter.get_errors():
                    all_errors.append(f"Issues with {os.path.basename(file_path)}:")
                    for error in converter.get_errors():
                        all_errors.append(f"  - {error}")
                else:
                    successful += 1
            except Exception as e:
                all_errors.append(f"Error processing {os.path.basename(file_path)}: {str(e)}")
        
        # Update status and show errors if any
        if all_errors:
            error_message = "\n".join(all_errors)
            QMessageBox.warning(self, "Conversion Issues", error_message)
            
        # Update status label
        if successful == len(self.selected_files):
            self.status_label.setText(f"Successfully converted {successful} files")
        else:
            self.status_label.setText(f"Converted {successful} of {len(self.selected_files)} files")
    
    def generate_hotspot_coordinates(self):
        """Run hotspot coordinates tool directly within the application"""
        # Ask user to select an image file
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image File",
            self.last_directory,
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )
        
        if not file_path:
            return  # User cancelled
            
        # Remember the directory for future file dialogs
        self.last_directory = os.path.dirname(file_path)
        
        try:
            # Show instructions to the user
            QMessageBox.information(
                self, 
                "Hotspot Coordinate Tool", 
                "The image will open in a new window.\n\n"
                "Click to add points to your polygon.\n\n"
                "Press any key to finish and display coordinates."
            )
            
            # Update status
            self.status_label.setText("Running image polygon tool...")
            
            # Run the hotspot polygon tool directly
            hotspot_tool = HotspotPolygonTool(file_path)
            percent_coords = hotspot_tool.run()
            
            # Format the coordinates as a string
            coordinates = "Polygon vertices (as percentages of width and height):\n"
            for coord in percent_coords:
                coordinates += f"{coord}\n"
            
            if not percent_coords:
                self.status_label.setText("No coordinates were generated")
                return
                
            # Show the coordinates in a dialog
            dialog = CoordinatesDialog(coordinates, self)
            dialog.exec()
            
            self.status_label.setText("Hotspot coordinates generated")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate hotspot coordinates: {str(e)}")
            self.status_label.setText("Error generating coordinates")

def run_gui():
    app = QApplication(sys.argv)
    window = QtiConverterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
