#!/usr/bin/env python3
"""
qti_gui.py

GUI interface for the QTI Converter application.
Provides a file selection dialog for selecting multiple .txt or .md files
to be converted to QTI format for Canvas LMS.
"""

import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                              QVBoxLayout, QLabel, QFileDialog, QWidget,
                              QListWidget, QHBoxLayout, QFrame)
from PySide6.QtCore import Qt
from qtiConverterApp import makeQti

class QtiConverterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTI Converter")
        self.setGeometry(100, 100, 600, 400)
        
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
        file_dialog.setDirectory(os.path.expanduser("~"))  # Start from home directory
        
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
    
    def convert_files(self):
        if not self.selected_files:
            self.status_label.setText("No files selected")
            return
        
        self.status_label.setText("Converting files...")
        successful = 0
        
        # Process each selected file
        for file_path in self.selected_files:
            try:
                # Default separator is '.'
                converter = makeQti(file_path, '.')
                converter.run()
                successful += 1
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        # Update status
        if successful == len(self.selected_files):
            self.status_label.setText(f"Successfully converted {successful} files")
        else:
            self.status_label.setText(f"Converted {successful} of {len(self.selected_files)} files")

def run_gui():
    app = QApplication(sys.argv)
    window = QtiConverterGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()
