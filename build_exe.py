import os
import sys
import subprocess
import shutil
import time
import stat
from pathlib import Path
import errno

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
            # Function to handle read-only files
            def on_rm_error(func, path, exc_info):
                # Change permissions and try again
                os.chmod(path, stat.S_IWRITE)
                try:
                    os.unlink(path)
                except Exception as e:
                    print(f"Warning: Could not remove {path}: {e}")
                    return
            
            try:
                shutil.rmtree(directory, onerror=on_rm_error)
                # Give Windows a moment to release file handles
                time.sleep(1)
            except Exception as e:
                print(f"Warning: Could not remove {directory}: {e}")
                print("Please make sure the application is not running and try again.")
                return False
    
    # Build the executable
    print("Creating executable...")
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--name=Easy',
        '--onefile',
        '--windowed',
        f'--icon={current_dir}/icon.ico',
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
            try:
                # Use start command to run in a new window
                if os.name == 'nt':  # Windows
                    os.startfile(exe_path)
                else:  # macOS and Linux
                    subprocess.Popen([str(exe_path)])
            except Exception as e:
                print(f"Error running executable: {e}")
                print("You can try running it manually from:", exe_path)
            
    except subprocess.CalledProcessError as e:
        print(f"Error during build: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("=== Building Easy Executable ===\n")
    if create_exe():
        input("\nPress Enter to exit...")
