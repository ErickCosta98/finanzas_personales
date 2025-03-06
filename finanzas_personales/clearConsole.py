import os
import platform
import subprocess

def clear_console():
    os_name = platform.system()
    
    if os_name == "Windows":
        # Detectar si se está usando PowerShell o CMD
        cmd = os.getenv('COMSPEC')
        if cmd and 'powershell' in cmd.lower():
            subprocess.run(["powershell", "-Command", "Clear-Host"], check=True)
        else:
            os.system("cls")
    else:
        # Para macOS y otros sistemas Unix/Linux, usamos 'clear'
        os.system("clear")
