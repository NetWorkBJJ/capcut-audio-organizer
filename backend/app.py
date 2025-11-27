from flask import Flask, render_template, request, jsonify
import sys
import os

# Add parent directory to path to import organize_audio
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from organize_audio import organize_audio, preview_changes

app = Flask(__name__, template_folder='../templates', static_folder='../static')

import tkinter as tk
from tkinter import filedialog

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pick-and-organize', methods=['POST'])
def pick_and_organize():
    try:
        # Open hidden tkinter window
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True) # Bring to front
        
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo do projeto CapCut",
            filetypes=[("CapCut Files", "*.json *.tmp"), ("All Files", "*.*")]
        )
        
        root.destroy()
        
        if not file_path:
            return jsonify({"success": False, "message": "Seleção cancelada."})
            
        # Run organization
        result = organize_audio(file_path)
        
        if result:
            return jsonify({
                "success": True, 
                "message": "Áudios organizados com sucesso!",
                "file": os.path.basename(file_path)
            })
        else:
            return jsonify({
                "success": True, 
                "message": "Nenhuma alteração foi necessária (já estava organizado).",
                "file": os.path.basename(file_path)
            })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Deprecated: Manual path upload
@app.route('/api/organize', methods=['POST'])
def organize():
    data = request.json
    file_path = data.get('filePath')
    
    if not file_path:
        return jsonify({"success": False, "message": "Nenhum caminho de arquivo fornecido."}), 400
        
    # Remove quotes if present
    file_path = file_path.replace("'", "").replace('"', "")
    
    if not os.path.exists(file_path):
        return jsonify({"success": False, "message": "Arquivo não encontrado."}), 404
        
    try:
        # Run the organization logic
        # Note: organize_audio prints to stdout, we might want to capture that or just rely on the return value
        # For now, we trust the return value
        result = organize_audio(file_path)
        
        if result:
            return jsonify({
                "success": True, 
                "message": "Áudios organizados com sucesso!",
                "file": os.path.basename(file_path)
            })
        else:
            return jsonify({
                "success": True, 
                "message": "Nenhuma alteração foi necessária (já estava organizado).",
                "file": os.path.basename(file_path)
            })
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

import webview
import threading
import time
import json

# ... (routes remain the same) ...

class Api:
    def __init__(self):
        self.selected_file = None

    def process_selected(self):
        """Process the previously selected/previewed file."""
        if not self.selected_file:
            return {"success": False, "message": "Nenhum arquivo selecionado."}
        
        try:
            success = organize_audio(self.selected_file)
            if success:
                return {"success": True, "message": "Áudios organizados com sucesso!"}
            else:
                return {"success": True, "message": "Nenhuma alteração necessária."}
        except Exception as e:
            return {"success": False, "message": str(e)}

    def pick_and_organize(self):
        """Open file picker and return preview of changes."""
        try:
            window = webview.windows[0]
            file_types = ('CapCut Files (*.json;*.tmp)', 'All Files (*.*)')
            
            # Default to CapCut projects folder
            import os.path
            capcut_path = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')
            initial_dir = capcut_path if os.path.exists(capcut_path) else os.path.expanduser('~')
            
            result = window.create_file_dialog(
                webview.OPEN_DIALOG, 
                allow_multiple=False, 
                file_types=file_types,
                directory=initial_dir
            )
            
            if not result:
                return {"success": False, "message": "Seleção cancelada."}
            
            file_path = result[0]
            self.selected_file = file_path
            
            # Get preview instead of processing immediately
            preview_result = preview_changes(file_path)
            
            if "error" in preview_result:
                return {"success": False, "message": preview_result["error"]}
            
            return {
                "success": True,
                "preview": True,
                "file": os.path.basename(file_path),
                "data": preview_result
            }
                
        except Exception as e:
            return {"success": False, "message": str(e)}

    def organize_path(self, file_path):
        # Allow JS to call this directly if it has a path (e.g. drag & drop)
        try:
            if not os.path.exists(file_path):
                return {"success": False, "message": "Arquivo não encontrado."}
                
            success = organize_audio(file_path)
            
            if success:
                return {"success": True, "message": "Áudios organizados com sucesso!"}
            else:
                return {"success": True, "message": "Nenhuma alteração necessária."}
        except Exception as e:
            return {"success": False, "message": str(e)}

def start_server():
    app.run(port=5000)

if __name__ == '__main__':
    print("Iniciando CapCut Audio Organizer...")
    
    api = Api()
    
    # Start Flask in a separate thread
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Wait a bit for server to start
    time.sleep(1)
    
    # Create native window with API
    webview.create_window(
        "CapCut Audio Organizer", 
        "http://127.0.0.1:5000",
        width=600,
        height=700,
        resizable=False,
        background_color='#0a0a0a',
        js_api=api
    )
    webview.start()
