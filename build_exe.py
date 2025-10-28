import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def create_exe():
    # Install PyInstaller if not installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        install_package('pyinstaller')
    
    # Get the current directory
    current_dir = Path(__file__).parent.absolute()
    script_path = current_dir / 'fl_plugin_remover.py'
    
    # Create build directory if it doesn't exist
    build_dir = current_dir / 'build'
    dist_dir = current_dir / 'dist'
    
    # Clean previous builds
    for directory in [build_dir, dist_dir]:
        if directory.exists():
            print(f"Removing existing {directory} directory...")
            shutil.rmtree(directory)
    
    # Build the executable
    print("Creating executable...")
    cmd = [
        'pyinstaller',
        '--name=Easy',
        '--onefile',
        '--windowed',
        '--icon=NONE',  # You can replace NONE with path to an .ico file if you have one
        '--clean',
        '--noconfirm',
        '--add-data', f'{script_path};.',
        str(script_path)
    ]
    
    try:
        subprocess.check_call(cmd, cwd=current_dir)
        print("\nBuild completed successfully!")
        print(f"Executable is located in: {dist_dir / 'Easy.exe'}")
        
        # Ask if user wants to run the executable
        run = input("\nDo you want to run the executable now? (y/n): ").strip().lower()
        if run == 'y':
            exe_path = dist_dir / 'Easy.exe'
            print(f"Running {exe_path}...")
            subprocess.Popen([exe_path])
            
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Building Easy Executable ===\n")
    if create_exe():
        input("\nPress Enter to exit...")
