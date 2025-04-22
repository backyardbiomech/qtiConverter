#!/usr/bin/env python3
"""
macOS-optimized build script for QTI Converter application
Uses a directory-based approach which often works better for PySide6 apps
"""

import os
import sys
import subprocess
import shutil
import platform
import tempfile

def main():
    print("==== Building QTI Converter for macOS (Directory Mode) ====")
    
    # Clean existing build artifacts
    for path in ["build", "dist"]:
        if os.path.exists(path):
            print(f"Cleaning {path} directory...")
            shutil.rmtree(path)
    
    # Remove any existing spec files
    for spec_file in ["QTI Converter.spec", "QTIConverter.spec"]:
        if os.path.exists(spec_file):
            print(f"Removing existing spec file: {spec_file}")
            os.remove(spec_file)
    
    # Get the project root directory
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Check for icon file
    icon_path = os.path.join(root_dir, "LargeIconQTI.icns")
    icon_option = f"--icon={icon_path}" if os.path.exists(icon_path) else ""
    
    print("\n== Creating macOS app using directory mode ==")
    
    # Create a temporary hook script to help PyInstaller find PySide6 modules
    hook_file = os.path.join(root_dir, "pyside6_hook.py")
    with open(hook_file, "w") as f:
        f.write("""
# PyInstaller hook for PySide6
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Add all PySide6 modules
hiddenimports = collect_submodules('PySide6')

# Add PySide6 data files
datas = collect_data_files('PySide6')
        """)
    
    # Build using direct PyInstaller command with optimized settings for macOS
    build_cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--name=QTIConverter",
        "--windowed",
        "--onedir",          # Use directory format which often works better for Qt apps
        "--clean",
        "--log-level=INFO",
        "--additional-hooks-dir=.",  # Use the hook we created
    ]
    
    # Add icon if it exists
    if os.path.exists(icon_path):
        build_cmd.append(f"--icon={icon_path}")
        
    # Add other options
    build_cmd.extend([
        "--osx-bundle-identifier=com.qticonverter.app",
        "--hidden-import=PySide6",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui", 
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=PySide6.support",
    ])
    
    # Add testFiles directory if it exists
    testfiles_dir = "testFiles"
    if os.path.exists(testfiles_dir):
        build_cmd.append(f"--add-data={testfiles_dir}:{testfiles_dir}")
    
    # Add main script
    build_cmd.append("main.py")
    
    print("Running build command:")
    print(" ".join(build_cmd))
    
    # Execute the build command
    try:
        result = subprocess.run(build_cmd, check=True)
        print("\n✅ Build completed successfully!")
        
        # Get the full path to the created app
        app_path = os.path.join(root_dir, "dist", "QTIConverter.app")
        if os.path.exists(app_path):
            print(f"\nThe application has been created at:\n{os.path.abspath(app_path)}")
            
            # Create a DMG for distribution
            print("\n== Creating DMG for easy distribution ==")
            
            # Create a temporary directory for DMG content
            with tempfile.TemporaryDirectory() as dmg_temp:
                # Copy the app to the temporary directory
                dmg_app_path = os.path.join(dmg_temp, "QTI Converter.app")
                shutil.copytree(app_path, dmg_app_path)
                
                # Create a symbolic link to /Applications folder
                os.symlink("/Applications", os.path.join(dmg_temp, "Applications"))
                
                # Create the DMG file
                dmg_path = os.path.join(root_dir, "dist", "QTI_Converter.dmg")
                if os.path.exists(dmg_path):
                    os.remove(dmg_path)
                
                dmg_cmd = [
                    "hdiutil",
                    "create",
                    "-volname", "QTI Converter",
                    "-srcfolder", dmg_temp,
                    "-ov",
                    "-format", "UDZO",
                    dmg_path
                ]
                
                try:
                    subprocess.run(dmg_cmd, check=True)
                    print(f"\n✅ DMG created at: {dmg_path}")
                    print("To install, open the DMG and drag QTI Converter to the Applications folder.")
                except subprocess.CalledProcessError:
                    print("⚠️ Failed to create DMG, but the app was successfully built.")
                    print("You can still copy the app to your Applications folder manually.")
                    
            print("\nTo install manually:")
            print(f"cp -R \"{app_path}\" /Applications/")
        else:
            print(f"\n⚠️ App not found at expected location: {app_path}")
    except subprocess.CalledProcessError as e:
        print("\n❌ Build failed")
        print(f"Error: {str(e)}")
        
    # Clean up hook file
    if os.path.exists(hook_file):
        os.remove(hook_file)

if __name__ == "__main__":
    main()
