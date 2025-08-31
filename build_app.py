"""
Build script for creating standalone Phin AI Assistant app
"""
import subprocess
import sys
import os

def create_launcher_script():
    """Create a launcher script for the Streamlit app"""
    launcher_content = '''#!/usr/bin/env python3
"""
Launcher for Phin AI Assistant
"""
import subprocess
import sys
import os
import webbrowser
import time
from threading import Thread

def run_streamlit():
    """Run the Streamlit app"""
    try:
        # Change to app directory
        app_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(app_dir)
        
        # Run streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "phin_main.py", "--server.headless", "true"], check=True)
    except Exception as e:
        print(f"Error running app: {e}")
        input("Press Enter to exit...")

def open_browser():
    """Open browser after delay"""
    time.sleep(3)
    webbrowser.open("http://localhost:8501")

if __name__ == "__main__":
    print("Starting Phin AI Assistant...")
    
    # Start browser opening in background
    browser_thread = Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Run the app
    run_streamlit()
'''
    
    with open('launcher.py', 'w') as f:
        f.write(launcher_content)
    print("Created launcher.py")

def build_executable():
    """Build executable using PyInstaller"""
    try:
        # Create launcher script
        create_launcher_script()
        
        # PyInstaller command
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name=PhinAI',
            '--add-data=phin_main.py:.',
            '--add-data=chat_handler.py:.',
            '--add-data=ui_components.py:.',
            '--add-data=config.py:.',
            '--add-data=styles.py:.',
            '--add-data=utils.py:.',
            '--add-data=memory.py:.',
            '--add-data=requirements.txt:.',
            '--hidden-import=streamlit',
            '--hidden-import=groq',
            '--collect-all=streamlit',
            'launcher.py'
        ]
        
        print("Building executable...")
        subprocess.run(cmd, check=True)
        print("Build complete! Check the 'dist' folder for PhinAI executable.")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    build_executable()
