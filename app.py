import os
import sys
import webview

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller .exe"""
    try:
        base_path = sys._MEIPASS  # PyInstaller extracts bundled files here
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# A lightweight, dedicated API class to handle saving safely
class PitwallApi:
    def save_backup(self, json_data):
        try:
            # Target the active Pitwall window
            window = webview.windows[0]
            
            # Trigger a native Windows 'Save As' dialog
            saved_file = window.create_file_dialog(
                webview.SAVE_DIALOG, 
                directory='', 
                save_filename='pitwall-backup.json'
            )
            
            # If a location is selected (and not cancelled)
            if saved_file and len(saved_file) > 0:
                with open(saved_file[0], 'w', encoding='utf-8') as f:
                    f.write(json_data)
                return "OK"
            return "CANCELLED"
        except Exception as e:
            return "ERROR"

if __name__ == "__main__":
    html_file = resource_path("pit-strategy-calculator.html")
    
    # Instantiate our API
    api = PitwallApi()
    
    webview.create_window(
        "Pitwall",
        html_file,
        js_api=api,  # Expose the API to the HTML environment
        width=1000,
        height=850,
        resizable=True,
        min_size=(600, 500)
    )
    
    # A safe fallback path pointing to: C:\Users\<Username>\AppData\Roaming\Pitwall
    appdata_path = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), 'Pitwall')

    # Start the application with absolute persistence enabled
    webview.start(
        private_mode=False,
        storage_path=appdata_path
    )