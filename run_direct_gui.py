#!/usr/bin/env python3
"""
Direct run script for QTI Converter GUI.
This bypasses PyInstaller and runs the GUI directly to help diagnose issues.
"""

import os
import sys
import traceback
from datetime import datetime

def main():
    # Set up error logging
    log_path = os.path.expanduser("~/Desktop/qticonverter_direct_run.log")
    with open(log_path, "w") as log_file:
        log_file.write(f"QTI Converter Direct Run Log - {datetime.now()}\n")
        log_file.write(f"Python version: {sys.version}\n")
        log_file.write(f"Working directory: {os.getcwd()}\n\n")
        
        try:
            # Try importing PySide6
            log_file.write("Importing PySide6...\n")
            try:
                import PySide6
                log_file.write(f"PySide6 version: {PySide6.__version__}\n")
            except Exception as e:
                log_file.write(f"Error importing PySide6: {str(e)}\n")
                log_file.write(traceback.format_exc())
                return 1
                
            # Import the necessary modules
            log_file.write("Importing PySide6 widgets...\n")
            try:
                from PySide6.QtWidgets import (
                    QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                    QLabel, QFileDialog, QWidget, QListWidget
                )
                from PySide6.QtCore import Qt
                log_file.write("Successfully imported PySide6 widgets\n")
            except Exception as e:
                log_file.write(f"Error importing PySide6 widgets: {str(e)}\n")
                log_file.write(traceback.format_exc())
                return 1
            
            # Create a basic GUI window for file selection
            log_file.write("Creating main application window...\n")
            app = QApplication(sys.argv)
            
            window = QMainWindow()
            window.setWindowTitle("QTI Converter (Direct Run)")
            window.setGeometry(100, 100, 600, 400)
            
            central_widget = QWidget()
            window.setCentralWidget(central_widget)
            layout = QVBoxLayout(central_widget)
            
            # Header
            title_label = QLabel("QTI Converter")
            title_label.setStyleSheet("font-size: 18pt; font-weight: bold;")
            title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title_label)
            
            # Description
            desc_label = QLabel("Select text files to convert to QTI format")
            desc_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(desc_label)
            
            # File list
            file_list = QListWidget()
            layout.addWidget(file_list)
            
            # Select files button
            select_button = QPushButton("Select Files")
            select_button.setMinimumHeight(40)
            
            def select_files():
                log_file.write("Select files button clicked\n")
                try:
                    file_dialog = QFileDialog(window)
                    file_dialog.setFileMode(QFileDialog.ExistingFiles)
                    file_dialog.setNameFilter("Text files (*.txt *.md)")
                    
                    if file_dialog.exec():
                        selected_files = file_dialog.selectedFiles()
                        file_list.clear()
                        for file_path in selected_files:
                            file_list.addItem(os.path.basename(file_path))
                        log_file.write(f"Selected {len(selected_files)} files\n")
                except Exception as e:
                    log_file.write(f"Error in file selection: {str(e)}\n")
                    log_file.write(traceback.format_exc())
            
            select_button.clicked.connect(select_files)
            layout.addWidget(select_button)
            
            # Status label
            status_label = QLabel("Ready")
            status_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(status_label)
            
            # Show the window
            log_file.write("Showing main window\n")
            window.show()
            
            # Run the application
            log_file.write("Starting application event loop\n")
            return app.exec()
            
        except Exception as e:
            log_file.write(f"Unexpected error: {str(e)}\n")
            log_file.write(traceback.format_exc())
            return 1

if __name__ == "__main__":
    sys.exit(main())
