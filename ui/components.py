"""
Premium UI Components - Componentes visuais customizados
"""

import tkinter as tk
from tkinter import Canvas


class PremiumButton(tk.Canvas):
    """Botao premium com hover effects e cantos arredondados."""

    def __init__(self, parent, text, command=None, theme=None, style='primary', width=200, height=45, **kwargs):
        super().__init__(parent, width=width, height=height, highlightthickness=0, **kwargs)

        self.theme = theme
        self.text = text
        self.command = command
        self.style = style
        self.width = width
        self.height = height
        self.enabled = True
        self.hover = False

        # Configura cores baseado no estilo
        self._setup_colors()

        # Desenha o botao
        self.draw()

        # Binds
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)

    def _setup_colors(self):
        """Configura cores baseado no estilo e tema."""
        if self.style == 'primary':
            self.bg_color = self.theme['accent']
            self.bg_hover = self.theme['accent_hover']
            self.fg_color = '#ffffff' if self.theme.is_dark() else '#ffffff'
        elif self.style == 'success':
            self.bg_color = self.theme['success']
            self.bg_hover = self.theme['success_hover']
            self.fg_color = '#ffffff'
        else:
            self.bg_color = self.theme['surface']
            self.bg_hover = self.theme['surface_hover']
            self.fg_color = self.theme['text_primary']

        self.bg_disabled = self.theme['surface_active']
        self.fg_disabled = self.theme['text_muted']

    def draw(self):
        """Desenha o botao."""
        self.delete('all')

        # Cor de fundo
        if not self.enabled:
            bg = self.bg_disabled
            fg = self.fg_disabled
        elif self.hover:
            bg = self.bg_hover
            fg = self.fg_color
        else:
            bg = self.bg_color
            fg = self.fg_color

        # Background do canvas
        self.configure(bg=self.theme['bg'])

        # Retangulo com cantos arredondados
        self._create_rounded_rect(2, 2, self.width-2, self.height-2, radius=10, fill=bg)

        # Texto
        self.create_text(
            self.width // 2, self.height // 2,
            text=self.text,
            font=('Segoe UI', 11, 'bold'),
            fill=fg
        )

    def _create_rounded_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """Cria um retangulo com cantos arredondados."""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1,
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def _on_enter(self, event):
        if self.enabled:
            self.hover = True
            self.draw()
            self.config(cursor='hand2')

    def _on_leave(self, event):
        self.hover = False
        self.draw()
        self.config(cursor='')

    def _on_click(self, event):
        if self.enabled and self.command:
            self.command()

    def set_enabled(self, enabled):
        """Ativa ou desativa o botao."""
        self.enabled = enabled
        self.draw()

    def update_theme(self, theme):
        """Atualiza o tema do botao."""
        self.theme = theme
        self._setup_colors()
        self.draw()


class DropZone(tk.Frame):
    """Area de drop/selecao de arquivo com visual premium."""

    def __init__(self, parent, theme, on_click=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = theme
        self.on_click = on_click
        self.hover = False

        self.configure(bg=self.theme['bg'])

        # Container com borda
        self.container = tk.Frame(self, bg=self.theme['surface'], padx=3, pady=3)
        self.container.pack(fill='both', expand=True, padx=20, pady=10)

        # Area interna
        self.inner = tk.Frame(self.container, bg=self.theme['surface'])
        self.inner.pack(fill='both', expand=True, padx=20, pady=25)

        # Icone (usando texto unicode)
        self.icon_label = tk.Label(
            self.inner,
            text="\u2191",  # Seta para cima
            font=('Segoe UI', 36),
            fg=self.theme['text_muted'],
            bg=self.theme['surface']
        )
        self.icon_label.pack(pady=(0, 10))

        # Texto principal
        self.title_label = tk.Label(
            self.inner,
            text="Clique para selecionar arquivo",
            font=('Segoe UI', 13, 'bold'),
            fg=self.theme['text_primary'],
            bg=self.theme['surface']
        )
        self.title_label.pack()

        # Texto secundario
        self.subtitle_label = tk.Label(
            self.inner,
            text="Arquivos suportados: .json, .tmp",
            font=('Segoe UI', 10),
            fg=self.theme['text_secondary'],
            bg=self.theme['surface']
        )
        self.subtitle_label.pack(pady=(5, 0))

        # Binds para hover
        for widget in [self, self.container, self.inner, self.icon_label, self.title_label, self.subtitle_label]:
            widget.bind('<Enter>', self._on_enter)
            widget.bind('<Leave>', self._on_leave)
            widget.bind('<Button-1>', self._on_click)

    def _on_enter(self, event):
        self.hover = True
        self.container.configure(bg=self.theme['accent'])
        self.inner.configure(bg=self.theme['surface_hover'])
        self.icon_label.configure(bg=self.theme['surface_hover'], fg=self.theme['accent'])
        self.title_label.configure(bg=self.theme['surface_hover'])
        self.subtitle_label.configure(bg=self.theme['surface_hover'])
        self.config(cursor='hand2')

    def _on_leave(self, event):
        self.hover = False
        self.container.configure(bg=self.theme['surface'])
        self.inner.configure(bg=self.theme['surface'])
        self.icon_label.configure(bg=self.theme['surface'], fg=self.theme['text_muted'])
        self.title_label.configure(bg=self.theme['surface'])
        self.subtitle_label.configure(bg=self.theme['surface'])
        self.config(cursor='')

    def _on_click(self, event):
        if self.on_click:
            self.on_click()

    def update_theme(self, theme):
        """Atualiza o tema."""
        self.theme = theme
        self.configure(bg=theme['bg'])
        self.container.configure(bg=theme['surface'])
        self.inner.configure(bg=theme['surface'])
        self.icon_label.configure(bg=theme['surface'], fg=theme['text_muted'])
        self.title_label.configure(bg=theme['surface'], fg=theme['text_primary'])
        self.subtitle_label.configure(bg=theme['surface'], fg=theme['text_secondary'])


class ClipList(tk.Frame):
    """Lista de clips com visual premium."""

    def __init__(self, parent, theme, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = theme
        self.configure(bg=self.theme['bg'])

        # Header
        self.header = tk.Frame(self, bg=self.theme['surface'], pady=8)
        self.header.pack(fill='x')

        self.header_title = tk.Label(
            self.header,
            text="Preview dos Clips",
            font=('Segoe UI', 11, 'bold'),
            fg=self.theme['text_primary'],
            bg=self.theme['surface']
        )
        self.header_title.pack(side='left', padx=15)

        self.header_count = tk.Label(
            self.header,
            text="0 clips",
            font=('Segoe UI', 10),
            fg=self.theme['text_secondary'],
            bg=self.theme['surface']
        )
        self.header_count.pack(side='right', padx=15)

        # Lista
        list_container = tk.Frame(self, bg=self.theme['border'])
        list_container.pack(fill='both', expand=True, padx=1, pady=(0, 1))

        # Scrollbar customizada
        self.scrollbar = tk.Scrollbar(list_container, bg=self.theme['surface'], troughcolor=self.theme['list_bg'])
        self.scrollbar.pack(side='right', fill='y')

        self.listbox = tk.Listbox(
            list_container,
            font=('Consolas', 10),
            bg=self.theme['list_bg'],
            fg=self.theme['text_primary'],
            selectbackground=self.theme['accent'],
            selectforeground='#ffffff',
            activestyle='none',
            relief='flat',
            bd=0,
            highlightthickness=0,
            height=10,
            yscrollcommand=self.scrollbar.set
        )
        self.listbox.pack(fill='both', expand=True, padx=10, pady=10)
        self.scrollbar.config(command=self.listbox.yview)

    def clear(self):
        """Limpa a lista."""
        self.listbox.delete(0, tk.END)
        self.header_count.config(text="0 clips")

    def add_clip(self, index, name, duration, will_move):
        """Adiciona um clip na lista."""
        status = "MOVER" if will_move else "OK"
        status_color = self.theme['warning'] if will_move else self.theme['success']
        line = f" {index:2}. {name[:28]:<28} {duration:>6.1f}s   [{status}]"
        self.listbox.insert(tk.END, line)

        if will_move:
            self.listbox.itemconfig(index - 1, fg=self.theme['warning'])
        else:
            self.listbox.itemconfig(index - 1, fg=self.theme['text_secondary'])

    def set_count(self, count):
        """Atualiza o contador de clips."""
        self.header_count.config(text=f"{count} clips")

    def update_theme(self, theme):
        """Atualiza o tema."""
        self.theme = theme
        self.configure(bg=theme['bg'])
        self.header.configure(bg=theme['surface'])
        self.header_title.configure(bg=theme['surface'], fg=theme['text_primary'])
        self.header_count.configure(bg=theme['surface'], fg=theme['text_secondary'])
        self.listbox.configure(
            bg=theme['list_bg'],
            fg=theme['text_primary'],
            selectbackground=theme['accent']
        )


class ThemeToggle(tk.Canvas):
    """Toggle switch para alternar entre dark/light mode."""

    def __init__(self, parent, theme, on_toggle=None, **kwargs):
        super().__init__(parent, width=70, height=32, highlightthickness=0, **kwargs)

        self.theme = theme
        self.on_toggle = on_toggle

        self.configure(bg=self.theme['bg'])
        self.draw()

        self.bind('<Button-1>', self._on_click)
        self.bind('<Enter>', lambda e: self.config(cursor='hand2'))
        self.bind('<Leave>', lambda e: self.config(cursor=''))

    def draw(self):
        """Desenha o toggle."""
        self.delete('all')

        is_dark = self.theme.is_dark()

        # Fundo do toggle
        bg_color = self.theme['surface']
        self.create_oval(2, 2, 30, 30, fill=bg_color, outline=self.theme['border'])
        self.create_oval(40, 2, 68, 30, fill=bg_color, outline=self.theme['border'])
        self.create_rectangle(16, 2, 54, 30, fill=bg_color, outline='')

        # Indicador ativo
        if is_dark:
            # Lua (dark mode ativo)
            self.create_oval(4, 4, 28, 28, fill=self.theme['accent'], outline='')
            self.create_text(16, 16, text="\u263D", font=('Segoe UI', 12), fill='#ffffff')
            self.create_text(54, 16, text="\u2600", font=('Segoe UI', 11), fill=self.theme['text_muted'])
        else:
            # Sol (light mode ativo)
            self.create_oval(42, 4, 66, 28, fill=self.theme['accent'], outline='')
            self.create_text(16, 16, text="\u263D", font=('Segoe UI', 12), fill=self.theme['text_muted'])
            self.create_text(54, 16, text="\u2600", font=('Segoe UI', 11), fill='#ffffff')

    def _on_click(self, event):
        if self.on_toggle:
            self.on_toggle()

    def update_theme(self, theme):
        """Atualiza o tema."""
        self.theme = theme
        self.configure(bg=theme['bg'])
        self.draw()


class StatusBar(tk.Frame):
    """Barra de status com visual premium."""

    def __init__(self, parent, theme, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = theme
        self.configure(bg=self.theme['bg'])

        # Container
        self.container = tk.Frame(self, bg=self.theme['surface'], pady=12)
        self.container.pack(fill='x')

        # Icone de status
        self.icon_label = tk.Label(
            self.container,
            text="\u25CF",  # Circulo
            font=('Segoe UI', 8),
            fg=self.theme['text_muted'],
            bg=self.theme['surface']
        )
        self.icon_label.pack(side='left', padx=(15, 8))

        # Texto de status
        self.status_label = tk.Label(
            self.container,
            text="Aguardando...",
            font=('Segoe UI', 10),
            fg=self.theme['text_secondary'],
            bg=self.theme['surface']
        )
        self.status_label.pack(side='left')

    def set_status(self, text, status_type='info'):
        """Atualiza o status."""
        self.status_label.config(text=text)

        colors = {
            'info': self.theme['text_muted'],
            'success': self.theme['success'],
            'warning': self.theme['warning'],
            'error': self.theme['error'],
            'processing': self.theme['accent']
        }

        color = colors.get(status_type, self.theme['text_muted'])
        self.icon_label.config(fg=color)
        self.status_label.config(fg=self.theme['text_secondary'])

    def update_theme(self, theme):
        """Atualiza o tema."""
        self.theme = theme
        self.configure(bg=theme['bg'])
        self.container.configure(bg=theme['surface'])
        self.icon_label.configure(bg=theme['surface'])
        self.status_label.configure(bg=theme['surface'], fg=theme['text_secondary'])


class InfoPanel(tk.Frame):
    """Painel de informacoes com estatisticas."""

    def __init__(self, parent, theme, **kwargs):
        super().__init__(parent, **kwargs)

        self.theme = theme
        self.configure(bg=self.theme['surface'], pady=12)

        # Container interno
        self.inner = tk.Frame(self, bg=self.theme['surface'])
        self.inner.pack(fill='x', padx=15)

        # Stats
        self.stats = []
        self._create_stat("Total", "0 clips")
        self._create_separator()
        self._create_stat("Duracao", "0.0s")
        self._create_separator()
        self._create_stat("A mover", "0")

    def _create_stat(self, label, value):
        """Cria uma estatistica."""
        frame = tk.Frame(self.inner, bg=self.theme['surface'])
        frame.pack(side='left', expand=True)

        label_widget = tk.Label(
            frame,
            text=label,
            font=('Segoe UI', 9),
            fg=self.theme['text_muted'],
            bg=self.theme['surface']
        )
        label_widget.pack()

        value_widget = tk.Label(
            frame,
            text=value,
            font=('Segoe UI', 12, 'bold'),
            fg=self.theme['text_primary'],
            bg=self.theme['surface']
        )
        value_widget.pack()

        self.stats.append((label_widget, value_widget))

    def _create_separator(self):
        """Cria um separador vertical."""
        sep = tk.Frame(self.inner, bg=self.theme['border'], width=1)
        sep.pack(side='left', fill='y', padx=15, pady=5)

    def set_stats(self, total, duration, to_move):
        """Atualiza as estatisticas."""
        if len(self.stats) >= 3:
            self.stats[0][1].config(text=f"{total} clips")
            self.stats[1][1].config(text=f"{duration:.1f}s")
            self.stats[2][1].config(text=str(to_move))

    def update_theme(self, theme):
        """Atualiza o tema."""
        self.theme = theme
        self.configure(bg=theme['surface'])
        self.inner.configure(bg=theme['surface'])
        for label, value in self.stats:
            label.configure(bg=theme['surface'], fg=theme['text_muted'])
            value.configure(bg=theme['surface'], fg=theme['text_primary'])
