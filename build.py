import os
import subprocess
import sys

def check_requirements():
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed.")
    except ImportError:
        print("⚙️ PyInstaller not found. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_app():
    print("🚀 Starting build process for Apex AI Bot...")
    
    # Define the PyInstaller command
    # --name: Name of the output executable
    # --windowed: Do not show a command prompt window (GUI only)
    # --onefile: Bundle everything into a single executable
    
    cmd = [
        "pyinstaller",
        "--name=Apex_AI_Bot",
        "--windowed", 
        "--onedir", 
        "--clean",
        "main.py"
    ]
    
    # NOTE: Used --onedir instead of --onefile. --onedir is faster to load and generally better for large PyQt apps.
    
    # Run PyInstaller
    subprocess.check_call(cmd)
    
    print("\n✅ Build completed successfully!")
    print("📁 You can find the executable in the 'dist/Apex_AI_Bot' folder.")
    print("⚠️ REMINDER: You MUST copy your '.env' file into the 'dist/Apex_AI_Bot' folder before running the executable, otherwise it will not have your API keys.")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    os.chdir(BASE_DIR)
    
    check_requirements()
    build_app()
