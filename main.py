"""
CapCut Audio Organizer - Apple Style Design
Clean, minimal, premium with rounded corners.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import json

# Path setup
if getattr(sys, 'frozen', False):
    APP_PATH = os.path.dirname(sys.executable)
    BUNDLE_PATH = sys._MEIPASS  # PyInstaller temp folder for bundled files
else:
    APP_PATH = os.path.dirname(os.path.abspath(__file__))
    BUNDLE_PATH = APP_PATH
sys.path.insert(0, APP_PATH)

from organizer import preview_changes, organize_audio, get_capcut_default_path, check_project_locked


# ============ TEMA ============
class Theme:
    DARK = {
        'bg': '#1c1c1e',
        'bg_secondary': '#2c2c2e',
        'bg_tertiary': '#3a3a3c',
        'card': '#2c2c2e',
        'card_hover': '#3a3a3c',
        'text': '#ffffff',
        'text_secondary': '#98989d',
        'text_tertiary': '#636366',
        'accent': '#0a84ff',
        'accent_hover': '#409cff',
        'success': '#30d158',
        'success_hover': '#28a745',
        'warning': '#ffd60a',
        'error': '#ff453a',
        'border': '#48484a',
        'divider': '#38383a',
    }

    LIGHT = {
        'bg': '#f2f2f7',
        'bg_secondary': '#ffffff',
        'bg_tertiary': '#e5e5ea',
        'card': '#ffffff',
        'card_hover': '#f2f2f7',
        'text': '#000000',
        'text_secondary': '#3c3c43',
        'text_tertiary': '#8e8e93',
        'accent': '#007aff',
        'accent_hover': '#0056b3',
        'success': '#34c759',
        'success_hover': '#2da44e',
        'warning': '#ff9500',
        'error': '#ff3b30',
        'border': '#d1d1d6',
        'divider': '#c6c6c8',
    }

    def __init__(self):
        self.is_dark = True
        self.colors = self.DARK.copy()
        self._load()

    def _load(self):
        try:
            cfg_path = os.path.join(APP_PATH, 'config.json')
            if os.path.exists(cfg_path):
                with open(cfg_path, 'r') as f:
                    cfg = json.load(f)
                    self.is_dark = cfg.get('dark_mode', True)
                    self.colors = self.DARK if self.is_dark else self.LIGHT
        except:
            pass

    def _save(self):
        try:
            cfg_path = os.path.join(APP_PATH, 'config.json')
            with open(cfg_path, 'w') as f:
                json.dump({'dark_mode': self.is_dark}, f)
        except:
            pass

    def toggle(self):
        self.is_dark = not self.is_dark
        self.colors = self.DARK if self.is_dark else self.LIGHT
        self._save()

    def __getitem__(self, key):
        return self.colors.get(key, '#ffffff')


# ============ ROUNDED CARD ============
class RoundedCard(tk.Canvas):
    """Card com cantos arredondados usando Canvas."""

    def __init__(self, parent, theme, radius=16, **kwargs):
        super().__init__(parent, highlightthickness=0, **kwargs)
        self.theme = theme
        self.radius = radius
        self.content_frame = None
        self._bg_rect = None

        self.configure(bg=theme['bg'])
        self.bind('<Configure>', self._on_resize)

    def _on_resize(self, event=None):
        self.delete('bg')
        w = self.winfo_width()
        h = self.winfo_height()
        if w > 1 and h > 1:
            self._draw_rounded_rect(0, 0, w, h, self.radius,
                                   fill=self.theme['card'],
                                   outline=self.theme['border'],
                                   width=1, tags='bg')
            if self.content_frame:
                self.tag_lower('bg')

    def _draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1,
            x2-r, y1,
            x2, y1,
            x2, y1+r,
            x2, y2-r,
            x2, y2,
            x2-r, y2,
            x1+r, y2,
            x1, y2,
            x1, y2-r,
            x1, y1+r,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def get_content_frame(self):
        if not self.content_frame:
            self.content_frame = tk.Frame(self, bg=self.theme['card'])
            self.create_window(self.radius, self.radius, window=self.content_frame, anchor='nw')
        return self.content_frame

    def update_theme(self, theme):
        self.theme = theme
        self.configure(bg=theme['bg'])
        if self.content_frame:
            self.content_frame.configure(bg=theme['card'])
        self._on_resize()


# ============ ROUNDED BUTTON ============
class RoundedButton(tk.Canvas):
    """Botao com cantos arredondados."""

    def __init__(self, parent, text, theme, style='primary', command=None,
                 width=200, height=48, radius=12, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)

        self.theme = theme
        self.text = text
        self.style = style
        self.command = command
        self.btn_width = width
        self.btn_height = height
        self.radius = radius
        self.enabled = True
        self.hover = False

        self._setup_colors()
        self.configure(bg=theme['bg'])
        self.draw()

        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)

    def _setup_colors(self):
        if self.style == 'primary':
            self.bg_normal = self.theme['accent']
            self.bg_hover = self.theme['accent_hover']
            self.fg_color = '#ffffff'
        elif self.style == 'success':
            self.bg_normal = self.theme['success']
            self.bg_hover = self.theme['success_hover']
            self.fg_color = '#ffffff'
        else:
            self.bg_normal = self.theme['bg_tertiary']
            self.bg_hover = self.theme['card_hover']
            self.fg_color = self.theme['text_tertiary']

        self.bg_disabled = self.theme['bg_tertiary']
        self.fg_disabled = self.theme['text_tertiary']

    def draw(self):
        self.delete('all')

        if not self.enabled:
            bg = self.bg_disabled
            fg = self.fg_disabled
        elif self.hover:
            bg = self.bg_hover
            fg = self.fg_color
        else:
            bg = self.bg_normal
            fg = self.fg_color

        # Rounded rectangle
        self._draw_rounded_rect(1, 1, self.btn_width-1, self.btn_height-1,
                               self.radius, fill=bg, outline='')

        # Text
        self.create_text(self.btn_width//2, self.btn_height//2, text=self.text,
                        font=('Segoe UI', 12, 'bold'), fill=fg)

    def _draw_rounded_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
            x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
            x1, y2, x1, y2-r, x1, y1+r, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, e):
        if self.enabled:
            self.hover = True
            self.draw()
            self.config(cursor='hand2')

    def _on_leave(self, e):
        self.hover = False
        self.draw()
        self.config(cursor='')

    def _on_click(self, e):
        if self.enabled and self.command:
            self.command()

    def set_enabled(self, enabled):
        self.enabled = enabled
        self.draw()

    def set_style(self, style):
        self.style = style
        self._setup_colors()
        self.draw()

    def update_theme(self, theme):
        self.theme = theme
        self._setup_colors()
        self.configure(bg=theme['bg'])
        self.draw()


# ============ APP ============
class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CapCut Audio Organizer")
        self.root.geometry("480x760")
        self.root.resizable(False, False)

        # Set window icon
        try:
            icon_path = os.path.join(BUNDLE_PATH, 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass

        self.theme = Theme()
        self.selected_file = None
        self.preview_data = None

        self._build_ui()
        self._center()

    def _center(self):
        self.root.update_idletasks()
        w, h = 480, 760
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')

    def _build_ui(self):
        self.root.configure(bg=self.theme['bg'])

        # Main container
        self.main = tk.Frame(self.root, bg=self.theme['bg'])
        self.main.pack(fill='both', expand=True, padx=24, pady=24)

        # Header
        self.header = tk.Frame(self.main, bg=self.theme['bg'])
        self.header.pack(fill='x', pady=(0, 8))

        self.title = tk.Label(self.header, text="Audio Organizer",
                        font=('Segoe UI', 24, 'bold'),
                        fg=self.theme['text'], bg=self.theme['bg'])
        self.title.pack(side='left')

        # Theme toggle button
        self.theme_btn = tk.Label(self.header, text="◐", font=('Segoe UI', 20),
                                  fg=self.theme['text_secondary'], bg=self.theme['bg'], cursor='hand2')
        self.theme_btn.pack(side='right')
        self.theme_btn.bind('<Button-1>', lambda e: self._toggle_theme())

        # Subtitle
        self.subtitle = tk.Label(self.main, text="Organize seus audios TTS do CapCut",
                           font=('Segoe UI', 11), fg=self.theme['text_secondary'], bg=self.theme['bg'])
        self.subtitle.pack(anchor='w', pady=(0, 20))

        # ===== CARD 1: File Selection =====
        self.card1_container = tk.Frame(self.main, bg=self.theme['bg'])
        self.card1_container.pack(fill='x', pady=(0, 16))

        self.card1 = tk.Frame(self.card1_container, bg=self.theme['card'],
                              highlightbackground=self.theme['border'], highlightthickness=1)
        self.card1.pack(fill='x', padx=2, pady=2)

        # Simular cantos arredondados com padding
        card1_inner = tk.Frame(self.card1, bg=self.theme['card'], padx=20, pady=20)
        card1_inner.pack(fill='x')

        # File icon and text
        file_row = tk.Frame(card1_inner, bg=self.theme['card'])
        file_row.pack(fill='x')

        self.icon_lbl = tk.Label(file_row, text="📁", font=('Segoe UI', 28), bg=self.theme['card'])
        self.icon_lbl.pack(side='left', padx=(0, 16))

        text_frame = tk.Frame(file_row, bg=self.theme['card'])
        text_frame.pack(side='left', fill='x', expand=True)

        self.file_title = tk.Label(text_frame, text="Nenhum arquivo selecionado",
                                   font=('Segoe UI', 14, 'bold'), fg=self.theme['text'],
                                   bg=self.theme['card'], anchor='w')
        self.file_title.pack(fill='x')

        self.file_subtitle = tk.Label(text_frame, text="Clique para selecionar um projeto",
                                      font=('Segoe UI', 11), fg=self.theme['text_secondary'],
                                      bg=self.theme['card'], anchor='w')
        self.file_subtitle.pack(fill='x')

        # Select button
        btn_frame = tk.Frame(card1_inner, bg=self.theme['card'])
        btn_frame.pack(fill='x', pady=(20, 0))

        self.btn_select = RoundedButton(btn_frame, "Selecionar Arquivo", self.theme,
                                        style='primary', command=self._select_file,
                                        width=396, height=48, radius=12)
        self.btn_select.pack()

        # ===== CARD 2: Preview =====
        self.card2_container = tk.Frame(self.main, bg=self.theme['bg'])
        self.card2_container.pack(fill='x', pady=(0, 16))

        self.card2 = tk.Frame(self.card2_container, bg=self.theme['card'],
                              highlightbackground=self.theme['border'], highlightthickness=1)
        self.card2.pack(fill='x', padx=2, pady=2)

        card2_inner = tk.Frame(self.card2, bg=self.theme['card'], padx=20, pady=16)
        card2_inner.pack(fill='x')

        # Preview header
        preview_header = tk.Frame(card2_inner, bg=self.theme['card'])
        preview_header.pack(fill='x', pady=(0, 12))

        self.preview_label = tk.Label(preview_header, text="Preview", font=('Segoe UI', 14, 'bold'),
                                      fg=self.theme['text'], bg=self.theme['card'])
        self.preview_label.pack(side='left')

        self.clip_count = tk.Label(preview_header, text="0 clips", font=('Segoe UI', 11),
                                   fg=self.theme['text_tertiary'], bg=self.theme['card'])
        self.clip_count.pack(side='right')

        # Listbox com scrollbar
        list_container = tk.Frame(card2_inner, bg=self.theme['border'])
        list_container.pack(fill='x')

        list_frame = tk.Frame(list_container, bg=self.theme['bg_secondary'])
        list_frame.pack(fill='x', padx=1, pady=1)

        # Scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(list_frame, font=('Consolas', 10),
                                  bg=self.theme['bg_secondary'], fg=self.theme['text'],
                                  selectbackground=self.theme['accent'],
                                  relief='flat', bd=0, highlightthickness=0,
                                  activestyle='none', height=10,
                                  yscrollcommand=scrollbar.set)
        self.listbox.pack(fill='x', expand=True)
        scrollbar.config(command=self.listbox.yview)

        self.list_frame = list_frame
        self.list_container = list_container

        # Stats row
        self.stats_frame = tk.Frame(card2_inner, bg=self.theme['card'])
        self.stats_frame.pack(fill='x', pady=(12, 0))

        self.stat_total = tk.Label(self.stats_frame, text="Total: -", font=('Segoe UI', 11),
                                   fg=self.theme['text_secondary'], bg=self.theme['card'])
        self.stat_total.pack(side='left')

        self.stat_duration = tk.Label(self.stats_frame, text="Duração: -", font=('Segoe UI', 11),
                                      fg=self.theme['text_secondary'], bg=self.theme['card'])
        self.stat_duration.pack(side='left', padx=(20, 0))

        self.stat_move = tk.Label(self.stats_frame, text="Mover: -", font=('Segoe UI', 11),
                                  fg=self.theme['text_secondary'], bg=self.theme['card'])
        self.stat_move.pack(side='left', padx=(20, 0))

        # ===== ACTION BUTTON =====
        btn_action_frame = tk.Frame(self.main, bg=self.theme['bg'])
        btn_action_frame.pack(fill='x', pady=(0, 16))

        self.btn_action = RoundedButton(btn_action_frame, "Organizar Audios", self.theme,
                                        style='disabled', command=self._organize,
                                        width=432, height=52, radius=14)
        self.btn_action.pack()
        self.btn_action_frame = btn_action_frame

        # ===== STATUS =====
        self.status = tk.Label(self.main, text="Aguardando seleção de arquivo...",
                              font=('Segoe UI', 10), fg=self.theme['text_tertiary'], bg=self.theme['bg'])
        self.status.pack()

        # ===== FOOTER =====
        self.footer = tk.Label(self.main, text="📍Criado por Anderson Network", font=('Segoe UI', 9),
                         fg=self.theme['text_tertiary'], bg=self.theme['bg'])
        self.footer.pack(pady=(8, 0))

        # Store frames for theme update
        self.card1_inner = card1_inner
        self.card2_inner = card2_inner
        self.file_row = file_row
        self.text_frame = text_frame
        self.preview_header = preview_header
        self.btn_frame = btn_frame

    def _toggle_theme(self):
        self.theme.toggle()
        self._apply_theme()

    def _apply_theme(self):
        t = self.theme

        # Root and main
        self.root.configure(bg=t['bg'])
        self.main.configure(bg=t['bg'])
        self.header.configure(bg=t['bg'])

        # Title and subtitle
        self.title.configure(fg=t['text'], bg=t['bg'])
        self.subtitle.configure(fg=t['text_secondary'], bg=t['bg'])
        self.theme_btn.configure(fg=t['text_secondary'], bg=t['bg'])

        # Card 1
        self.card1_container.configure(bg=t['bg'])
        self.card1.configure(bg=t['card'], highlightbackground=t['border'])
        self.card1_inner.configure(bg=t['card'])
        self.file_row.configure(bg=t['card'])
        self.icon_lbl.configure(bg=t['card'])
        self.text_frame.configure(bg=t['card'])
        self.file_title.configure(fg=t['text'], bg=t['card'])
        self.file_subtitle.configure(fg=t['text_secondary'], bg=t['card'])
        self.btn_frame.configure(bg=t['card'])
        self.btn_select.update_theme(t)

        # Card 2
        self.card2_container.configure(bg=t['bg'])
        self.card2.configure(bg=t['card'], highlightbackground=t['border'])
        self.card2_inner.configure(bg=t['card'])
        self.preview_header.configure(bg=t['card'])
        self.preview_label.configure(fg=t['text'], bg=t['card'])
        self.clip_count.configure(fg=t['text_tertiary'], bg=t['card'])
        self.list_container.configure(bg=t['border'])
        self.list_frame.configure(bg=t['bg_secondary'])
        self.listbox.configure(bg=t['bg_secondary'], fg=t['text'], selectbackground=t['accent'])

        # Stats
        self.stats_frame.configure(bg=t['card'])
        self.stat_total.configure(fg=t['text_secondary'], bg=t['card'])
        self.stat_duration.configure(fg=t['text_secondary'], bg=t['card'])
        self.stat_move.configure(fg=t['text_secondary'], bg=t['card'])

        # Action button
        self.btn_action_frame.configure(bg=t['bg'])
        self.btn_action.update_theme(t)

        # Status and footer
        self.status.configure(fg=t['text_tertiary'], bg=t['bg'])
        self.footer.configure(fg=t['text_tertiary'], bg=t['bg'])

        # Re-color listbox items
        if self.preview_data and 'clips' in self.preview_data:
            for i, clip in enumerate(self.preview_data['clips']):
                if clip['will_move']:
                    self.listbox.itemconfig(i, fg=t['warning'])

    def _enable_action(self, enabled):
        if enabled:
            self.btn_action.set_style('success')
            self.btn_action.set_enabled(True)
        else:
            self.btn_action.set_style('disabled')
            self.btn_action.set_enabled(False)

    def _select_file(self):
        path = filedialog.askopenfilename(
            title="Selecione o projeto CapCut",
            initialdir=get_capcut_default_path(),
            filetypes=[("Arquivos CapCut", "*.json;*.tmp"), ("Todos", "*.*")]
        )

        if not path:
            return

        self.selected_file = path
        filename = os.path.basename(path)
        self.file_title.config(text=filename)
        self.file_subtitle.config(text="Analisando...")
        self.status.config(text="Analisando arquivo...")
        self.root.update()

        # Preview
        self.preview_data = preview_changes(path)
        self.listbox.delete(0, tk.END)

        if "error" in self.preview_data:
            self.file_subtitle.config(text="Erro ao ler arquivo")
            self.status.config(text=self.preview_data['error'])
            self._enable_action(False)
            messagebox.showerror("Erro", self.preview_data['error'])
            return

        total = self.preview_data['total_clips']

        if total == 0:
            self.file_subtitle.config(text="Nenhum audio TTS encontrado")
            self.status.config(text="Nenhum audio TTS encontrado")
            self.clip_count.config(text="0 clips")
            self._enable_action(False)
            return

        # Populate list
        for i, clip in enumerate(self.preview_data['clips'], 1):
            status = "→" if clip['will_move'] else "✓"
            line = f"  {i:2}. {clip['name'][:25]:<25}  {clip['duration_sec']:>5.1f}s  {status}"
            self.listbox.insert(tk.END, line)
            if clip['will_move']:
                self.listbox.itemconfig(i-1, fg=self.theme['warning'])

        # Update stats
        duration = self.preview_data['total_duration_sec']
        to_move = sum(1 for c in self.preview_data['clips'] if c['will_move'])

        self.clip_count.config(text=f"{total} clips")
        self.stat_total.config(text=f"Total: {total}")
        self.stat_duration.config(text=f"Duração: {duration:.0f}s")
        self.stat_move.config(text=f"Mover: {to_move}")

        if self.preview_data['will_modify']:
            self.file_subtitle.config(text=f"{to_move} clips precisam ser movidos")
            self.status.config(text="Pronto para organizar")
            self._enable_action(True)
        else:
            self.file_subtitle.config(text="Já está organizado!")
            self.status.config(text="Audios já estão organizados")
            self._enable_action(False)

    def _organize(self):
        if not self.selected_file:
            return

        if check_project_locked(self.selected_file):
            messagebox.showwarning("Projeto Aberto",
                "Feche o projeto no CapCut antes de continuar.")
            return

        if not messagebox.askyesno("Confirmar",
            f"Reorganizar {self.preview_data['total_clips']} clips?"):
            return

        self.status.config(text="Processando...")
        self.root.update()

        success, msg = organize_audio(self.selected_file)

        if success:
            self.status.config(text="Concluído com sucesso!")
            messagebox.showinfo("Sucesso", msg + "\n\nReabra o projeto no CapCut.")

            # Reset
            self.listbox.delete(0, tk.END)
            self.file_title.config(text="Nenhum arquivo selecionado")
            self.file_subtitle.config(text="Clique para selecionar um projeto")
            self.clip_count.config(text="0 clips")
            self.stat_total.config(text="Total: -")
            self.stat_duration.config(text="Duração: -")
            self.stat_move.config(text="Mover: -")
            self.selected_file = None
            self.preview_data = None
            self._enable_action(False)
            self.status.config(text="Aguardando seleção de arquivo...")
        else:
            self.status.config(text="Erro no processamento")
            messagebox.showerror("Erro", msg)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
