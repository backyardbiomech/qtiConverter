#!/usr/bin/env python3
"""
Simplified debug version of the QTI Converter main script.
This version includes error logging and creates a basic test window.
"""

import os
import sys
import traceback

def setup_error_logging():
    """Configure error logging to a file for debugging"""
    # Create logs directory if it doesn't exist
    log_dir = os.path.expanduser("~/Desktop")
    log_path = os.path.join(log_dir, "qticonverter_error.log")
    
    # Redirect stderr to log file
    sys.stderr = open(log_path, "w")
    
    print(f"Starting QTI Converter (Debug Mode)")
    print(f"Error log: {log_path}")
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    print(f"Script path: {os.path.abspath(__file__)}")
    print(f"Working directory: {os.getcwd()}")
    print(f"sys.path: {sys.path}")
    return log_path

def main():
    """Run a simplified QTI Converter test application with error handling"""
    log_path = setup_error_logging()
    
    try:
        print("Importing required modules...")
        
        # Try importing modules one by one to identify issues
        print("Importing PySide6...")
        import PySide6
        print(f"PySide6 version: {PySide6.__version__}")
        
        # Import only the widgets we need for the test
        from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget
        from PySide6.QtCore import Qt
        print("PySide6 modules imported successfully")
        
        # Create a simple test window to verify PySide6 is working properly
        print("Creating test window...")
        app = QApplication(sys.argv)
        window = QMainWindow()
        window.setWindowTitle("QTI Converter Test")
        window.setGeometry(100, 100, 400, 200)
        
        # Create central widget and layout
        central_widget = QWidget()
        window.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add a label
        label = QLabel("QTI Converter Debug Test")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Add a button
        button = QPushButton("Close")
        button.clicked.connect(window.close)
        layout.addWidget(button)
        
        # Show window
        print("Showing test window...")
        window.show()
        
        print("Starting application event loop...")
        return app.exec()
        
    except Exception as e:
        error_msg = f"ERROR: {str(e)}\n\n{traceback.format_exc()}"
        print(error_msg, file=sys.stderr)
        
        # Also try to show an error dialog
        try:
            from PySide6.QtWidgets import QApplication, QMessageBox
            app = QApplication.instance() or QApplication(sys.argv)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("QTI Converter Error")
            msg.setInformativeText(str(e))
            msg.setDetailedText(traceback.format_exc())
            msg.setWindowTitle("Error Starting QTI Converter")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()
        except Exception:
            pass
            
        print(f"\nError log written to: {log_path}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
