"""
CapCut Audio Organizer - Logica de Organizacao
Reorganiza audios TTS (Text-to-Speech) do CapCut em uma unica trilha sequencial.
"""

import json
import os
import time


def preview_changes(file_path):
    """
    Analisa o arquivo JSON do CapCut e retorna preview das alteracoes.
    Nao modifica nada, apenas le e calcula.

    Args:
        file_path: Caminho do arquivo JSON do projeto CapCut

    Returns:
        dict com informacoes dos clips TTS encontrados
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return {"error": f"Arquivo JSON invalido: {e}"}
    except Exception as e:
        return {"error": f"Erro ao ler arquivo: {e}"}

    # 1. Encontra materiais de audio TTS
    materials = data.get('materials', {})
    audios = materials.get('audios', [])
    tts_material_ids = set()
    material_names = {}

    for audio in audios:
        if audio.get('type') == 'text_to_audio':
            mat_id = audio.get('id')
            tts_material_ids.add(mat_id)
            material_names[mat_id] = audio.get('name', 'Clip sem nome')

    if not tts_material_ids:
        return {
            "total_clips": 0,
            "will_modify": False,
            "clips": [],
            "message": "Nenhum audio TTS encontrado neste projeto."
        }

    # 2. Encontra segmentos que usam esses materiais
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
                        'name': material_names.get(mat_id, 'Clip sem nome')
                    })

    if not all_tts_segments:
        return {
            "total_clips": 0,
            "will_modify": False,
            "clips": [],
            "message": "Nenhum segmento TTS encontrado nas trilhas."
        }

    # 3. Ordena por tempo de inicio atual
    all_tts_segments.sort(key=lambda x: x['segment']['target_timerange']['start'])

    # 4. Calcula novos tempos (sequenciais)
    current_time = all_tts_segments[0]['segment']['target_timerange']['start'] if all_tts_segments else 0
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
            'current_start_us': current_start,
            'new_start_us': current_time,
            'duration_us': duration,
            'current_start_sec': current_start / 1_000_000,
            'new_start_sec': current_time / 1_000_000,
            'duration_sec': duration / 1_000_000,
            'will_move': would_change
        })

        current_time += duration

    return {
        "total_clips": len(clips_info),
        "will_modify": will_modify,
        "clips": clips_info,
        "total_duration_sec": total_duration_us / 1_000_000,
        "message": "Analise concluida com sucesso."
    }


def organize_audio(file_path):
    """
    Reorganiza os audios TTS do CapCut em uma unica trilha sequencial.

    Args:
        file_path: Caminho do arquivo JSON do projeto CapCut

    Returns:
        tuple (success: bool, message: str)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return False, f"Arquivo JSON invalido: {e}"
    except Exception as e:
        return False, f"Erro ao ler arquivo: {e}"

    # 1. Identifica materiais TTS
    materials = data.get('materials', {})
    audios = materials.get('audios', [])
    tts_material_ids = set()
    material_names = {}

    for audio in audios:
        if audio.get('type') == 'text_to_audio':
            mat_id = audio.get('id')
            tts_material_ids.add(mat_id)
            material_names[mat_id] = audio.get('name', 'Clip sem nome')

    if not tts_material_ids:
        return False, "Nenhum audio TTS encontrado neste projeto."

    # 2. Coleta todos os segmentos TTS de todas as tracks
    tracks = data.get('tracks', [])
    all_tts_segments = []

    for track in tracks:
        if track.get('type') == 'audio':
            segments = track.get('segments', [])
            for segment in segments:
                mat_id = segment.get('material_id')
                if mat_id in tts_material_ids:
                    all_tts_segments.append(segment)

    if not all_tts_segments:
        return False, "Nenhum segmento TTS encontrado nas trilhas."

    # 3. Ordena por tempo de inicio
    all_tts_segments.sort(key=lambda x: x['target_timerange']['start'])

    # 4. Encontra a primeira track de audio (master track)
    master_track = None
    for track in tracks:
        if track.get('type') == 'audio':
            master_track = track
            break

    if not master_track:
        return False, "Nenhuma trilha de audio encontrada no projeto."

    # 5. Remove segmentos TTS de TODAS as tracks
    for track in tracks:
        if track.get('type') == 'audio':
            new_segments = []
            for seg in track.get('segments', []):
                if seg.get('material_id') not in tts_material_ids:
                    new_segments.append(seg)
            track['segments'] = new_segments

    # 6. Adiciona segmentos organizados na master track
    current_time = all_tts_segments[0]['target_timerange']['start'] if all_tts_segments else 0

    for segment in all_tts_segments:
        timerange = segment['target_timerange']
        duration = timerange['duration']

        # Atualiza tempo de inicio
        segment['target_timerange']['start'] = current_time

        # Adiciona na master track
        master_track['segments'].append(segment)

        current_time += duration

    # 7. Ordena segmentos da master track
    master_track['segments'].sort(key=lambda x: x['target_timerange']['start'])

    # 8. Salva arquivos - SINCRONIZA TODOS OS ARQUIVOS DO PROJETO
    dir_path = os.path.dirname(os.path.abspath(file_path))

    try:
        # Lista de arquivos principais que precisam ser sincronizados
        files_to_sync = [
            file_path,  # Arquivo selecionado pelo usuario
            os.path.join(dir_path, "draft_content.json"),
            os.path.join(dir_path, "template-2.tmp"),
        ]

        # IMPORTANTE: Sincronizar arquivos na pasta Timelines
        # O CapCut le os arquivos de dentro desta pasta!
        timelines_dir = os.path.join(dir_path, "Timelines")
        if os.path.exists(timelines_dir):
            for item in os.listdir(timelines_dir):
                timeline_subdir = os.path.join(timelines_dir, item)
                if os.path.isdir(timeline_subdir):
                    files_to_sync.append(os.path.join(timeline_subdir, "draft_content.json"))
                    files_to_sync.append(os.path.join(timeline_subdir, "template-2.tmp"))

        # Salva em todos os arquivos que existem
        for sync_path in files_to_sync:
            if os.path.exists(sync_path) or sync_path == file_path:
                try:
                    with open(sync_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, separators=(',', ':'))
                except Exception:
                    pass  # Continua tentando os outros arquivos

        # Atualiza timestamp no draft_meta_info.json
        draft_meta_path = os.path.join(dir_path, "draft_meta_info.json")
        if os.path.exists(draft_meta_path):
            try:
                with open(draft_meta_path, 'r', encoding='utf-8') as f:
                    meta_data = json.load(f)

                current_timestamp = int(time.time() * 1_000_000)
                meta_data['tm_draft_modified'] = current_timestamp

                with open(draft_meta_path, 'w', encoding='utf-8') as f:
                    json.dump(meta_data, f, separators=(',', ':'))
            except Exception:
                pass  # Ignora erros no metadata

        # Limpa cache do CapCut (forca reload)
        draft_extra_path = os.path.join(dir_path, "draft.extra")
        if os.path.exists(draft_extra_path):
            try:
                extra_backup = draft_extra_path + ".backup"
                if os.path.exists(extra_backup):
                    os.remove(extra_backup)
                os.rename(draft_extra_path, extra_backup)
            except Exception:
                pass  # Ignora erro se nao conseguir renomear

    except Exception as e:
        return False, f"Erro ao salvar arquivos: {e}"

    return True, f"Audios organizados com sucesso! {len(all_tts_segments)} clips reorganizados."


def get_capcut_default_path():
    """
    Retorna o caminho padrao dos projetos do CapCut no Windows.

    Returns:
        str: Caminho do diretorio de projetos do CapCut
    """
    local_app_data = os.environ.get('LOCALAPPDATA', '')

    # Caminho correto do CapCut no Windows
    capcut_path = os.path.join(local_app_data, 'CapCut Drafts')

    if os.path.exists(capcut_path):
        return capcut_path

    return os.path.expanduser('~')


def check_project_locked(file_path):
    """
    Verifica se o projeto esta aberto no CapCut.

    Args:
        file_path: Caminho do arquivo do projeto

    Returns:
        bool: True se o projeto esta bloqueado (CapCut aberto)
    """
    dir_path = os.path.dirname(os.path.abspath(file_path))
    locked_path = os.path.join(dir_path, '.locked')
    return os.path.exists(locked_path)
