import json
import os
import shutil
import sys

# Removed top-level tkinter imports to avoid conflicts with pywebview

def organize_audio(file_path):
    # ... (rest of function) ...
    # Backup original file
    backup_path = file_path + ".backup"
    if not os.path.exists(backup_path):
        shutil.copy(file_path, backup_path)
        print(f"Backup created at {backup_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Identify text-to-audio materials and map IDs to Names
    materials = data.get('materials', {})
    audios = materials.get('audios', [])
    tts_material_ids = set()
    material_names = {}
    
    for audio in audios:
        if audio.get('type') == 'text_to_audio':
            mat_id = audio.get('id')
            tts_material_ids.add(mat_id)
            material_names[mat_id] = audio.get('name', 'Unknown Clip')
            
    if not tts_material_ids:
        print("No text-to-audio materials found.")
        return False

    # 2. Collect all segments that use these materials
    tracks = data.get('tracks', [])
    all_tts_segments = []

    for track in tracks:
        if track.get('type') == 'audio':
            segments = track.get('segments', [])
            for segment in segments:
                mat_id = segment.get('material_id')
                if mat_id in tts_material_ids:
                    # Attach name for logging
                    segment['_debug_name'] = material_names.get(mat_id)
                    all_tts_segments.append(segment)

    if not all_tts_segments:
        print("No segments found using text-to-audio materials.")
        return False

    # 3. Sort all segments by their current start time
    all_tts_segments.sort(key=lambda x: x['target_timerange']['start'])

    # 4. Update start times sequentially AND move to the first audio track
    current_time = 0
    modified = False
    
    if all_tts_segments:
        current_time = all_tts_segments[0]['target_timerange']['start']

    print(f"Found {len(all_tts_segments)} audio clips. Organizing into Single Track...")

    # Find the first audio track to be the "Master Track"
    master_track = None
    for track in tracks:
        if track.get('type') == 'audio':
            master_track = track
            break
            
    if not master_track:
        print("Error: No audio track found to merge into.")
        return False

    # Clear text-to-audio segments from ALL tracks first
    # We will re-add them to the master track later
    for track in tracks:
        if track.get('type') == 'audio':
            # Keep only segments that are NOT text-to-audio
            # (We identified text-to-audio by checking if they were in all_tts_segments)
            # A safer way is checking material_id again
            new_segments = []
            for seg in track.get('segments', []):
                if seg.get('material_id') not in tts_material_ids:
                    new_segments.append(seg)
            track['segments'] = new_segments

    # Now add organized segments to master_track
    for i, segment in enumerate(all_tts_segments):
        timerange = segment['target_timerange']
        duration = timerange['duration']
        start = timerange['start']
        name = segment.get('_debug_name')
        
        # Force start time
        if start != current_time:
            # print(f"Moving '{name}' to {current_time}")
            segment['target_timerange']['start'] = current_time
            modified = True
        
        # Clean up debug key
        if '_debug_name' in segment:
            del segment['_debug_name']
            
        # Add to master track
        master_track['segments'].append(segment)
        
        current_time += duration
        
    # Ensure master track segments are sorted (CapCut might prefer this)
    master_track['segments'].sort(key=lambda x: x['target_timerange']['start'])
    
    # Always mark as modified if we did the merge logic, just to be safe
    modified = True

    # Determine directory and file paths
    dir_path = os.path.dirname(os.path.abspath(file_path))
    draft_info_path = os.path.join(dir_path, "draft_info.json")
    
    # Define files to update (current selected + draft_info if exists)
    files_to_update = [file_path]
    if os.path.exists(draft_info_path) and os.path.abspath(file_path) != os.path.abspath(draft_info_path):
        files_to_update.append(draft_info_path)

    # Update draft_meta_info.json timestamp
    draft_meta_path = os.path.join(dir_path, "draft_meta_info.json")
    if os.path.exists(draft_meta_path):
        try:
            with open(draft_meta_path, 'r', encoding='utf-8') as f:
                meta_data = json.load(f)
            
            # Update timestamp (microseconds)
            import time
            current_timestamp = int(time.time() * 1000000)
            meta_data['tm_draft_modified'] = current_timestamp
            
            # Create backup
            if not os.path.exists(draft_meta_path + ".backup"):
                shutil.copy(draft_meta_path, draft_meta_path + ".backup")
                
            with open(draft_meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta_data, f, separators=(',', ':'))
            print(f"Updated timestamp in: {os.path.basename(draft_meta_path)}")
        except Exception as e:
            print(f"Failed to update metadata: {e}")

    if modified:
        for f_path in files_to_update:
            # Create backup
            if not os.path.exists(f_path + ".backup"):
                shutil.copy(f_path, f_path + ".backup")
            
            # Save minified JSON
            with open(f_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, separators=(',', ':'))
            print(f"Updated file: {os.path.basename(f_path)}")
            
        print("All files synchronized.")
    else:
        print("JSON structure is already organized.")

    # ALWAYS clear draft.extra cache if we are in a project folder
    draft_extra_path = os.path.join(dir_path, "draft.extra")
    if os.path.exists(draft_extra_path):
        extra_backup = draft_extra_path + ".backup"
        if os.path.exists(extra_backup):
            os.remove(extra_backup)
        os.rename(draft_extra_path, extra_backup)
        print(f"Cache cleared: Renamed draft.extra to {os.path.basename(extra_backup)} to force reload.")
        return True # Return True because we did something useful (cleared cache)
        
    return modified

def preview_changes(file_path):
    """
    Analyze the file and return a preview of what would be changed.
    Returns a dict with:
    - total_clips: number of audio clips
    - will_modify: whether changes are needed
    - clips: list of clip info (name, current_start, new_start, duration)
    - total_duration: total duration in seconds
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        return {"error": str(e)}

    materials = data.get('materials', {})
    audios = materials.get('audios', [])
    tts_material_ids = set()
    material_names = {}
    
    for audio in audios:
        if audio.get('type') == 'text_to_audio':
            mat_id = audio.get('id')
            tts_material_ids.add(mat_id)
            material_names[mat_id] = audio.get('name', 'Unknown Clip')
    
    if not tts_material_ids:
        return {"total_clips": 0, "will_modify": False, "clips": [], "message": "Nenhum áudio de texto-para-fala encontrado."}
    
    tracks = data.get('tracks', [])
    all_tts_segments = []
    
    for track in tracks:
        if track.get('type') == 'audio':
            segments = track.get('segments', [])
            for segment in segments:
                mat_id = segment.get('material_id')
                if mat_id in tts_material_ids:
                    all_tts_segments.append({
                        'segment': segment,
                        'name': material_names.get(mat_id, 'Unknown')
                    })
    
    if not all_tts_segments:
        return {"total_clips": 0, "will_modify": False, "clips": [], "message": "Nenhum segmento encontrado."}
    
    all_tts_segments.sort(key=lambda x: x['segment']['target_timerange']['start'])
    
    # Calculate what would change
    current_time = 0
    if all_tts_segments:
        current_time = all_tts_segments[0]['segment']['target_timerange']['start']
    
    will_modify = False
    clips_info = []
    total_duration_us = 0
    
    for item in all_tts_segments:
        segment = item['segment']
        name = item['name']
        timerange = segment['target_timerange']
        duration = timerange['duration']
        current_start = timerange['start']
        
        total_duration_us += duration
        
        would_change = current_start != current_time
        if would_change:
            will_modify = True
        
        clips_info.append({
            'name': name,
            'current_start_sec': current_start / 1000000,
            'new_start_sec': current_time / 1000000,
            'duration_sec': duration / 1000000,
            'will_move': would_change
        })
        
        current_time += duration
    
    return {
        "total_clips": len(clips_info),
        "will_modify": will_modify,
        "clips": clips_info,
        "total_duration_sec": total_duration_us / 1000000
    }

def check_for_newer_files(selected_file):
    directory = os.path.dirname(selected_file)
    if not directory:
        directory = "."
        
    selected_mtime = os.path.getmtime(selected_file)
    newer_files = []
    
    for f in os.listdir(directory):
        if f.endswith('.json') or f.endswith('.tmp'):
            full_path = os.path.join(directory, f)
            if full_path != selected_file and os.path.getmtime(full_path) > selected_mtime:
                newer_files.append(f)
                
    if newer_files:
        print("\n⚠️  AVISO: Existem arquivos mais recentes nesta pasta!")
        print("O CapCut pode estar usando um destes ao invés do que você selecionou:")
        for nf in newer_files:
            print(f" - {nf}")
        print("-" * 30 + "\n")
        return True
    return False

def list_backups(file_path):
    """List all backup files in the same directory."""
    dir_path = os.path.dirname(os.path.abspath(file_path))
    backups = []
    
    for f in os.listdir(dir_path):
        if f.endswith('.backup'):
            full_path = os.path.join(dir_path, f)
            stat = os.stat(full_path)
            backups.append({
                'name': f,
                'path': full_path,
                'size': stat.st_size,
                'modified': stat.st_mtime
            })
    
    return sorted(backups, key=lambda x: x['modified'], reverse=True)

def restore_backup(backup_path):
    """Restore a backup file."""
    if not os.path.exists(backup_path):
        return {"success": False, "message": "Backup não encontrado"}
    
    # Get original filename (remove .backup extension)
    original_path = backup_path.replace('.backup', '')
    
    try:
        # Backup the current file before restoring
        if os.path.exists(original_path):
            temp_backup = original_path + '.pre-restore-backup'
            shutil.copy(original_path, temp_backup)
        
        # Restore
        shutil.copy(backup_path, original_path)
        
        return {
            "success": True, 
            "message": f"Backup restaurado: {os.path.basename(original_path)}"
        }
    except Exception as e:
        return {"success": False, "message": str(e)}

def setup_logging():
    """Setup logging system."""
    import logging
    from logging.handlers import RotatingFileHandler
    
    log_dir = os.path.expanduser('~/.capcut_organizer/logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'app.log')
    
    handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    logger = logging.getLogger('capcut_organizer')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    
    return logger

import sys

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog, messagebox

    print("--- CapCut Audio Organizer ---")
    
    target_file = ""
    
    # Check for command line argument
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Create hidden root window
        root = tk.Tk()
        root.withdraw()
        print("Selecione o arquivo do projeto (draft_content.json ou template-2.tmp)...")
        target_file = filedialog.askopenfilename(
            title="Selecione o arquivo do projeto CapCut",
            filetypes=[("CapCut Files", "*.json *.tmp"), ("All Files", "*.*")]
        )

    if target_file:
        # Remove quotes if the user dragged and dropped the file
        target_file = target_file.replace("'", "").replace('"', "")
        abs_path = os.path.abspath(target_file)
        
        print(f"\n📂 Arquivo Selecionado: {abs_path}")
        
        if "Antigravidade" in abs_path:
            print("\n⚠️  ALERTA: Você selecionou um arquivo dentro da pasta 'Antigravidade'.")
            print("Para que funcione no CapCut, você deve selecionar o arquivo ORIGINAL dentro da pasta do CapCut.")
            print("Caminho esperado algo como: .../Movies/CapCut/User Data/Projects/...\n")
            confirm = input("Deseja continuar mesmo assim? (s/n): ").strip().lower()
            if confirm != 's':
                print("Operação cancelada.")
                sys.exit(0)
        
        # Check for newer files
        has_newer = check_for_newer_files(target_file)
        
        try:
            if organize_audio(target_file):
                msg = f"Áudios organizados com sucesso!\n\nArquivo atualizado: {os.path.basename(target_file)}\nBackup criado: {os.path.basename(target_file)}.backup"
                
                if has_newer:
                    msg += "\n\n⚠️ ATENÇÃO: Existem arquivos mais recentes na pasta. Verifique o terminal."
                
                if "Antigravidade" in abs_path:
                    msg += "\n\n⚠️ ALERTA: Arquivo na pasta de scripts (Antigravidade). Certifique-se de copiar para a pasta do CapCut."

                print(msg)
                # Only show messagebox if not using CLI
                if len(sys.argv) == 1:
                    messagebox.showinfo("Sucesso", msg)
            else:
                msg = "Nenhuma alteração foi necessária."
                print(msg)
                if len(sys.argv) == 1:
                    messagebox.showinfo("Info", msg)
        except Exception as e:
            err_msg = f"Ocorreu um erro:\n{str(e)}"
            print(err_msg)
            if len(sys.argv) == 1:
                messagebox.showerror("Erro", err_msg)
    else:
        print("Nenhum arquivo selecionado.")
