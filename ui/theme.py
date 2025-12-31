"""
Theme Manager - Gerenciamento de temas Dark/Light
"""

import json
import os

# Paleta Dark Mode
DARK_THEME = {
    'name': 'dark',
    'bg': '#0f0f0f',
    'bg_secondary': '#141414',
    'surface': '#1a1a1a',
    'surface_hover': '#252525',
    'surface_active': '#2a2a2a',
    'border': '#2a2a2a',
    'border_light': '#333333',
    'text_primary': '#ffffff',
    'text_secondary': '#a0a0a0',
    'text_muted': '#666666',
    'accent': '#00d4ff',
    'accent_hover': '#00b8e6',
    'accent_muted': '#00d4ff33',
    'success': '#10b981',
    'success_hover': '#059669',
    'warning': '#f59e0b',
    'error': '#ef4444',
    'list_bg': '#0d1117',
    'list_alt': '#161b22',
    'list_hover': '#1f2937',
    'scrollbar': '#333333',
    'scrollbar_hover': '#444444',
}

# Paleta Light Mode
LIGHT_THEME = {
    'name': 'light',
    'bg': '#f5f5f7',
    'bg_secondary': '#ebebed',
    'surface': '#ffffff',
    'surface_hover': '#f0f0f0',
    'surface_active': '#e5e5e5',
    'border': '#e5e5e5',
    'border_light': '#d1d1d1',
    'text_primary': '#1a1a1a',
    'text_secondary': '#6b7280',
    'text_muted': '#9ca3af',
    'accent': '#0099ff',
    'accent_hover': '#0077cc',
    'accent_muted': '#0099ff22',
    'success': '#059669',
    'success_hover': '#047857',
    'warning': '#d97706',
    'error': '#dc2626',
    'list_bg': '#ffffff',
    'list_alt': '#f9fafb',
    'list_hover': '#f3f4f6',
    'scrollbar': '#d1d5db',
    'scrollbar_hover': '#9ca3af',
}


class Theme:
    """Gerenciador de temas da aplicacao."""

    def __init__(self, config_path=None):
        self.config_path = config_path or self._get_default_config_path()
        self.current_theme = DARK_THEME
        self.load_preference()

    def _get_default_config_path(self):
        """Retorna o caminho padrao do arquivo de configuracao."""
        import sys
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, 'config.json')

    def load_preference(self):
        """Carrega a preferencia de tema do usuario."""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    if config.get('theme') == 'light':
                        self.current_theme = LIGHT_THEME
                    else:
                        self.current_theme = DARK_THEME
        except Exception:
            self.current_theme = DARK_THEME

    def save_preference(self):
        """Salva a preferencia de tema do usuario."""
        try:
            config = {'theme': self.current_theme['name']}
            with open(self.config_path, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass

    def toggle(self):
        """Alterna entre dark e light mode."""
        if self.current_theme['name'] == 'dark':
            self.current_theme = LIGHT_THEME
        else:
            self.current_theme = DARK_THEME
        self.save_preference()
        return self.current_theme

    def is_dark(self):
        """Verifica se o tema atual e dark."""
        return self.current_theme['name'] == 'dark'

    def get(self, key, default=None):
        """Retorna uma cor do tema atual."""
        return self.current_theme.get(key, default)

    def __getitem__(self, key):
        """Permite acessar cores como theme['bg']."""
        return self.current_theme[key]
