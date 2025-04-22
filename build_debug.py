#!/usr/bin/env python3
"""
Debug build script for QTI Converter application
Creates a version with error logging to help diagnose startup issues
"""

import os
import sys
import subprocess
import platform
import shutil
import importlib.util

# First, clean up any previous spec files that might be causing conflicts
def clean_spec_files():
    for spec_file in ["QTIConverterDebug.spec"]:
        if os.path.exists(spec_file):
            print(f"Removing old spec file: {spec_file}")
            os.remove(spec_file)

def main():
    print("Starting debug build process for QTI Converter...")
    
    # Clean up old spec files first
    clean_spec_files()
    
    # Clean existing build artifacts
    build_dir = "build"
    dist_dir = "dist"
    if os.path.exists(build_dir):
        print("Cleaning existing build directory...")
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        print("Cleaning existing dist directory...")
        shutil.rmtree(dist_dir)
    
    # Determine system-specific options
    is_mac = platform.system() == "Darwin"
    
    # Debug build command - using a simpler approach to avoid symlink issues
    command = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=QTIConverterDebug",
        "--onefile",         # Use onefile to avoid symlink issues with Qt frameworks
        "--noconsole",       # Use noconsole for Mac instead of windowed
        "--noconfirm",
        "--clean",           # Clean PyInstaller cache
        "--debug=imports",   # Debug imports which is most useful for our case
        "--log-level=INFO"   # Less verbose logging
    ]
    
    # Add Mac-specific options
    if is_mac:
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "LargeIconQTI.icns")
        if os.path.exists(icon_path):
            command.append("--icon=" + icon_path)
            print("Using icon file:", icon_path)
    
    # Add data files
    testfiles_dir = "testFiles"
    if os.path.exists(testfiles_dir):
        if is_mac:
            command.append("--add-data=" + testfiles_dir + ":" + testfiles_dir)
        else:
            command.append("--add-data=" + testfiles_dir + ";" + testfiles_dir)
    
    # Add all required dependencies, including OpenCV for the hotspot coordinates feature
    command.extend([
        "--hidden-import=PySide6", 
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=re",
        "--hidden-import=html",
        "--hidden-import=os",
        "--hidden-import=sys",
        "--hidden-import=cv2",
        "--hidden-import=numpy",
        "--hidden-import=pathlib",
        "--collect-all=PySide6",
        "--collect-all=cv2",
    ])
    
    # Use the debug main.py
    command.append("debug_main.py")
    
    # Print the command for debugging
    print("Running command:")
    print(" ".join(command))
    
    # Run PyInstaller
    try:
        print("\n--- STARTING DEBUG BUILD ---\n")
        result = subprocess.run(command, check=False)
        
        # Check if the build was successful
        if result.returncode == 0:
            print("\n--- DEBUG BUILD COMPLETED SUCCESSFULLY ---\n")
            
            # For onefile mode, the executable is directly in the dist directory
            if is_mac:
                exe_path = os.path.join("dist", "QTIConverterDebug")
                if os.path.exists(exe_path):
                    print(f"The debug application has been created at: {os.path.abspath(exe_path)}")
                    
                    # Create a shell script to run with terminal output
                    script_path = os.path.join("dist", "run_debug_qti.sh")
                    with open(script_path, "w") as f:
                        f.write("#!/bin/bash\n")
                        f.write(f"cd \"{os.path.dirname(os.path.abspath(exe_path))}\"\n")
                        f.write(f"./QTIConverterDebug\n")
                    
                    # Make the script executable
                    os.chmod(script_path, 0o755)
                    os.chmod(exe_path, 0o755)  # Make sure the executable has correct permissions
                    print(f"Created debug launch script at: {os.path.abspath(script_path)}")
                    print("Run this script in a terminal to see error output.")
                else:
                    print("Warning: Expected executable not found at", exe_path)
                    
            print("\nINSTRUCTIONS:")
            print("1. Run the debug version of the app")
            print("2. Check your Desktop for the qticonverter_error.log file")
            print("3. If a log file appears, check it for error details")
            print("4. If no log appears, the app may be missing critical files")
                    
        else:
            print("\n--- DEBUG BUILD FAILED ---")
            print(f"PyInstaller returned error code: {result.returncode}")
            
    except Exception as e:
        print(f"Error running PyInstaller: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
