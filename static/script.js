// DOM Elements
const dropZone = document.getElementById('dropZone');
const historySection = document.getElementById('historySection');
const historyList = document.getElementById('historyList');
const themeToggle = document.getElementById('themeToggle');
const previewModal = document.getElementById('previewModal');
const processingModal = document.getElementById('processingModal');
const btnCancelPreview = document.getElementById('btnCancelPreview');
const btnConfirmProcess = document.getElementById('btnConfirmProcess');
const btnReset = document.getElementById('btnReset');
const spinner = document.getElementById('spinner');
const successIcon = document.getElementById('successIcon');
const statusTitle = document.getElementById('statusTitle');
const statusMessage = document.getElementById('statusMessage');

// History Management
const HISTORY_KEY = 'capcut_organizer_history';
const THEME_KEY = 'capcut_organizer_theme';

function loadHistory() {
    const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    if (history.length > 0) {
        historySection.style.display = 'block';
        historyList.innerHTML = '';

        history.slice(0, 5).forEach(item => {
            const div = document.createElement('div');
            div.className = 'history-item';
            div.innerHTML = `
                <span class="history-item-name">${item.name}</span>
                <span class="history-item-time">${timeAgo(item.timestamp)}</span>
            `;
            div.onclick = () => processFile(item.path);
            historyList.appendChild(div);
        });
    }
}

function addToHistory(path, name, success) {
    const history = JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]');
    history.unshift({
        path: path,
        name: name,
        timestamp: Date.now(),
        success: success
    });
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 10)));
    loadHistory();
}

function timeAgo(timestamp) {
    const seconds = Math.floor((Date.now() - timestamp) / 1000);
    if (seconds < 60) return 'agora';
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m atrás`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h atrás`;
    return `${Math.floor(seconds / 86400)}d atrás`;
}

// Theme Management
function loadTheme() {
    const theme = localStorage.getItem(THEME_KEY) || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
}

themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem(THEME_KEY, newTheme);
});

// Confetti Celebration
function celebrate() {
    const count = 200;
    const defaults = {
        origin: { y: 0.7 }
    };

    function fire(particleRatio, opts) {
        confetti({
            ...defaults,
            ...opts,
            particleCount: Math.floor(count * particleRatio),
            colors: ['#00F0FF', '#7000FF', '#FF00FF', '#00FFFF']
        });
    }

    fire(0.25, { spread: 26, startVelocity: 55 });
    fire(0.2, { spread: 60 });
    fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 });
    fire(0.1, { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 });
    fire(0.1, { spread: 120, startVelocity: 45 });
}

// File Selection
dropZone.addEventListener('click', () => {
    if (!window.pywebview) {
        alert('Sistema inicializando...');
        return;
    }

    showProcessing('Aguardando Seleção...', 'Selecione o arquivo na janela que abriu.');

    window.pywebview.api.pick_and_organize()
        .then(data => {
            if (data.success && data.preview) {
                hideProcessing();
                showPreview(data.data, data.file);
            } else if (data.success) {
                celebrate();
                showSuccess(data.message);
            } else {
                if (data.message.includes('cancelada')) {
                    hideProcessing();
                } else {
                    showError(data.message);
                }
            }
        })
        .catch(err => {
            showError('Erro interno: ' + err);
        });
});

// Preview Modal
function showPreview(data, filename) {
    document.getElementById('previewTotalClips').textContent = data.total_clips;
    document.getElementById('previewDuration').textContent = data.total_duration_sec.toFixed(1) + 's';
    document.getElementById('previewWillModify').textContent = data.will_modify ? 'Sim ✓' : 'Já organizado';

    const clipsList = document.getElementById('previewClipsList');
    clipsList.innerHTML = '';

    if (data.clips && data.clips.length > 0) {
        data.clips.forEach((clip, idx) => {
            const div = document.createElement('div');
            div.className = 'clip-item' + (clip.will_move ? ' will-move' : '');
            div.innerHTML = `
                <strong>${idx + 1}. ${clip.name}</strong><br>
                <small>${clip.will_move ? '→ Movendo' : 'OK'} | Duração: ${clip.duration_sec.toFixed(1)}s</small>
            `;
            clipsList.appendChild(div);
        });
    }

    previewModal.classList.add('active');
}

function hidePreview() {
    previewModal.classList.remove('active');
}

btnCancelPreview.addEventListener('click', hidePreview);

btnConfirmProcess.addEventListener('click', () => {
    hidePreview();
    showProcessing('Processando...', 'Organizando áudios...');

    window.pywebview.api.process_selected()
        .then(data => {
            if (data.success) {
                celebrate();
                showSuccess(data.message);
            } else {
                showError(data.message);
            }
        })
        .catch(err => {
            showError('Erro interno: ' + err);
        });
});

// Processing Modal
function showProcessing(title, message) {
    spinner.style.display = 'block';
    successIcon.style.display = 'none';
    btnReset.style.display = 'none';
    statusTitle.textContent = title;
    statusMessage.textContent = message;
    processingModal.classList.add('active');
}

function hideProcessing() {
    processingModal.classList.remove('active');
}

function showSuccess(message) {
    spinner.style.display = 'none';
    successIcon.style.display = 'flex';
    btnReset.style.display = 'block';
    statusTitle.textContent = 'Sucesso!';
    statusMessage.textContent = message;
}

function showError(message) {
    spinner.style.display = 'none';
    successIcon.style.display = 'none';
    btnReset.style.display = 'block';
    statusTitle.textContent = 'Erro';
    statusMessage.textContent = message;
}

btnReset.addEventListener('click', () => {
    hideProcessing();
});

// Initialize
loadTheme();
loadHistory();
