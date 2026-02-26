let currentMode = 'lessons';
let currentLessonType = null;
let currentLessonIndex = null;
let currentPattern = '';
let patternIndex = 0;
let lessonErrors = 0;
let lessonTotal = 0;

let selectedLanguage = 'english';
let selectedDifficulty = null;
let selectedTrainMode = 'full';
let selectedDuration = 2;
let textContent = '';
let textIndex = 0;
let textErrors = 0;
let textTotal = 0;
let timerInterval = null;
let timeRemaining = 0;
let startTime = null;
let textActive = false;
let currentTextIndex = 0;
let allTexts = {};

let dvorakToQwertys = {};
let soundsEnabled = true;

function loadFromStorage(key, defaultValue) {
    try {
        const stored = localStorage.getItem('dvorak_' + key);
        return stored ? JSON.parse(stored) : defaultValue;
    } catch (e) {
        return defaultValue;
    }
}

function saveToStorage(key, value) {
    try {
        localStorage.setItem('dvorak_' + key, JSON.stringify(value));
    } catch (e) {
        console.error('Failed to save to localStorage:', e);
    }
}

let completedLessons = new Set(loadFromStorage('completed_lessons', []));
let sessionResults = loadFromStorage('session_results', []);
let errorLetters = loadFromStorage('error_letters', {});

async function init() {
    await loadKeymap();
    await loadLessons();
    setupEventListeners();
    highlightHomeRow();
    updateStatsDisplay();
    updateSoundButton();
}

async function loadKeymap() {
    try {
        const [dvormapRes, homerowRes] = await Promise.all([
            fetch('/api/dvormap'),
            fetch('/api/homerow')
        ]);
        dvorakToQwertys = await dvormapRes.json();
        const homeRowDvorak = await homerowRes.json();
        window.HOME_ROW_DVORAK = homeRowDvorak;
    } catch (e) {
        console.error('Failed to load keymap:', e);
        window.HOME_ROW_DVORAK = ['a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's'];
    }
}

async function loadLessons() {
    try {
        const [res2, res4, resWords, textsRes] = await Promise.all([
            fetch('/api/lessons/2letter'),
            fetch('/api/lessons/4letter'),
            fetch('/api/lessons/words'),
            fetch('/api/texts')
        ]);
        const lessons2 = await res2.json();
        const lessons4 = await res4.json();
        const lessonsWords = await resWords.json();
        allTexts = await textsRes.json();

        renderLessonButtons('lessons-2', lessons2, '2letter');
        renderLessonButtons('lessons-4', lessons4, '4letter');
        renderLessonButtons('lessons-words', lessonsWords, 'words');
    } catch (e) {
        console.error('Failed to load lessons:', e);
    }
}

function renderLessonButtons(containerId, lessons, type) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    lessons.forEach((lesson, index) => {
        const btn = document.createElement('button');
        btn.className = 'lesson-btn';
        const lessonKey = `${type}-${index}`;
        if (completedLessons.has(lessonKey)) {
            btn.innerHTML = `${lesson.pattern} 🏆`;
        } else {
            btn.textContent = lesson.pattern;
        }
        btn.title = lesson.name;
        btn.dataset.type = type;
        btn.dataset.index = index;
        btn.addEventListener('click', () => startLesson(type, index));
        container.appendChild(btn);
    });
}

function setupEventListeners() {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => switchMode(tab.dataset.mode));
    });

    document.querySelectorAll('.language-btn').forEach(btn => {
        btn.addEventListener('click', () => selectLanguage(btn.dataset.lang));
    });

    document.querySelectorAll('.difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => selectDifficulty(btn.dataset.diff));
    });

    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => selectTrainMode(btn.dataset.train));
    });

    document.querySelectorAll('.duration-btn').forEach(btn => {
        btn.addEventListener('click', () => selectDuration(parseInt(btn.dataset.time)));
    });

    document.getElementById('lesson-input').addEventListener('input', handleLessonInput);
    document.getElementById('text-input').addEventListener('input', handleTextInput);
    document.getElementById('reset-lesson').addEventListener('click', resetLesson);
    document.getElementById('reset-text').addEventListener('click', resetText);
    document.getElementById('try-again').addEventListener('click', () => {
        document.getElementById('results-area').style.display = 'none';
        document.getElementById('text-area').style.display = 'block';
    });

    document.getElementById('toggle-sounds').addEventListener('click', toggleSounds);
    document.getElementById('reset-progress').addEventListener('click', resetAllProgress);

    document.addEventListener('keydown', handleKeyDown);
    document.addEventListener('keyup', handleKeyUp);
}

function toggleSounds() {
    soundsEnabled = !soundsEnabled;
    saveToStorage('sounds_enabled', soundsEnabled);
    updateSoundButton();
}

function updateSoundButton() {
    const btn = document.getElementById('toggle-sounds');
    btn.textContent = soundsEnabled ? 'Enabled' : 'Disabled';
    btn.classList.toggle('active', soundsEnabled);
}

function playSound(type) {
    if (!soundsEnabled) return;
    
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    if (type === 'error') {
        oscillator.frequency.value = 200;
        oscillator.type = 'square';
        gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.3);
        oscillator.start(audioCtx.currentTime);
        oscillator.stop(audioCtx.currentTime + 0.3);
    } else if (type === 'success') {
        oscillator.frequency.value = 523.25;
        oscillator.type = 'sine';
        gainNode.gain.setValueAtTime(0.3, audioCtx.currentTime);
        oscillator.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1);
        oscillator.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.4);
        oscillator.start(audioCtx.currentTime);
        oscillator.stop(audioCtx.currentTime + 0.4);
    }
}

function resetAllProgress() {
    if (confirm('Are you sure you want to reset all progress? This cannot be undone.')) {
        completedLessons.clear();
        sessionResults = [];
        errorLetters = {};
        saveToStorage('completed_lessons', []);
        saveToStorage('session_results', []);
        saveToStorage('error_letters', {});
        
        document.querySelectorAll('.lesson-btn').forEach(btn => {
            btn.innerHTML = btn.textContent.replace(' 🏆', '');
        });
        
        updateStatsDisplay();
        alert('All progress has been reset.');
    }
}

function updateStatsDisplay() {
    const totalSessions = sessionResults.length;
    const bestWpm = sessionResults.reduce((max, r) => Math.max(max, r.wpm), 0);
    const avgAccuracy = totalSessions > 0 
        ? Math.round(sessionResults.reduce((sum, r) => sum + r.accuracy, 0) / totalSessions) 
        : 0;
    const lessonsCompleted = completedLessons.size;

    document.getElementById('total-sessions').textContent = totalSessions;
    document.getElementById('best-wpm').textContent = bestWpm;
    document.getElementById('avg-accuracy').textContent = avgAccuracy + '%';
    document.getElementById('lessons-completed').textContent = lessonsCompleted;

    const historyBody = document.getElementById('history-body');
    historyBody.innerHTML = '';
    
    sessionResults.slice(-20).reverse().forEach(r => {
        const row = document.createElement('tr');
        const typeLabel = r.type === 'text' ? 'Text' : 'Lesson';
        const modeLabel = r.mode === 'timer' ? `${r.duration}m` : 'Full';
        const date = new Date(r.timestamp).toLocaleDateString();
        row.innerHTML = `
            <td>${typeLabel}</td>
            <td>${r.difficulty || '-'}</td>
            <td>${modeLabel}</td>
            <td>${r.wpm}</td>
            <td>${r.accuracy}%</td>
            <td>${date}</td>
        `;
        historyBody.appendChild(row);
    });
    
    updateStrugglingLetters();
}

function updateStrugglingLetters() {
    const chart = document.getElementById('struggling-letters-chart');
    if (!chart) return;
    
    const sorted = Object.entries(errorLetters)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);
    
    if (sorted.length === 0) {
        chart.innerHTML = '<p class="no-data">No error data yet</p>';
        return;
    }
    
    const maxErrors = sorted[0][1];
    
    chart.innerHTML = sorted.map(([letter, count]) => `
        <div class="struggling-letter-row">
            <span class="struggling-letter">${letter}</span>
            <div class="struggling-bar-container">
                <div class="struggling-bar" style="width: ${(count / maxErrors) * 100}%"></div>
            </div>
            <span class="struggling-count">${count}</span>
        </div>
    `).join('');
}

function switchMode(mode) {
    currentMode = mode;
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');
    document.querySelectorAll('.mode-content').forEach(c => c.classList.remove('active'));
    document.getElementById(`${mode}-mode`).classList.add('active');
    
    if (mode === 'stats') {
        updateStatsDisplay();
    }
}

function selectLanguage(lang) {
    selectedLanguage = lang;
    document.querySelectorAll('.language-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.language-btn[data-lang="${lang}"]`).classList.add('active');
    
    if (selectedDifficulty) {
        selectDifficulty(selectedDifficulty);
    }
}

function dvorakToQwerty(dvorakChar) {
    return dvorakToQwertys[dvorakChar.toLowerCase()] || dvorakChar.toLowerCase();
}

function startLesson(type, index) {
    currentLessonType = type;
    currentLessonIndex = index;

    document.querySelectorAll('.lesson-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.lesson-btn[data-type="${type}"][data-index="${index}"]`).classList.add('active');

    fetch(`/api/lessons/${type}`)
        .then(res => res.json())
        .then(lessons => {
            const lesson = lessons[index];
            currentPattern = lesson.pattern;
            patternIndex = 0;
            lessonErrors = 0;
            lessonTotal = 0;

            document.getElementById('lesson-name').textContent = lesson.name;
            document.getElementById('lesson-prompt').textContent = generateLessonText(currentPattern, 10);
            document.getElementById('accuracy').textContent = '0%';
            document.getElementById('errors').textContent = '0';
            document.getElementById('lesson-input').value = '';
            document.getElementById('lesson-area').style.display = 'block';
            document.getElementById('lesson-input').focus();

            highlightKeys(currentPattern);
        });
}

function generateLessonText(pattern, count) {
    const parts = [];
    for (let i = 0; i < count; i++) {
        parts.push(pattern);
    }
    return parts.join(' ');
}

function highlightKeys(pattern) {
    document.querySelectorAll('.key').forEach(k => k.classList.remove('highlight'));
    const uniqueChars = [...new Set(pattern)];
    uniqueChars.forEach(char => {
        const qwertyKey = dvorakToQwerty(char);
        const keyElement = document.querySelector(`.key[data-key="${qwertyKey}"]`);
        if (keyElement) {
            keyElement.classList.add('highlight');
        }
    });
}

function handleLessonInput(e) {
    const input = e.target;
    const value = input.value;
    const expectedChar = currentPattern[patternIndex % currentPattern.length];

    lessonTotal++;

    if (value.length > 0) {
        const lastChar = value[value.length - 1];
        if (lastChar === expectedChar) {
            input.classList.remove('error');
            input.classList.add('correct');
            patternIndex++;
            updateLessonDisplay();
        } else {
            input.classList.remove('correct');
            input.classList.add('error');
            lessonErrors++;
            playSound('error');
            setTimeout(() => input.classList.remove('error'), 300);
        }
    }

    updateLessonStats();

    if (patternIndex >= currentPattern.length * 10) {
        setTimeout(() => {
            const accuracy = Math.round(((lessonTotal - lessonErrors) / lessonTotal) * 100);
            if (accuracy >= 90 && currentLessonIndex !== null) {
                const lessonKey = `${currentLessonType}-${currentLessonIndex}`;
                if (!completedLessons.has(lessonKey)) {
                    completedLessons.add(lessonKey);
                    saveToStorage('completed_lessons', Array.from(completedLessons));
                    updateLessonButtonsWithTrophies();
                }
                playSound('success');
                
                if (currentLessonType === '2letter' && currentLessonIndex < 19) {
                    startLesson('2letter', currentLessonIndex + 1);
                } else if (currentLessonType === '4letter' && currentLessonIndex < 25) {
                    startLesson('4letter', currentLessonIndex + 1);
                } else if (currentLessonType === 'words' && currentLessonIndex < 19) {
                    startLesson('words', currentLessonIndex + 1);
                } else {
                    alert('Lesson completed! Great job! 🏆');
                }
            } else {
                resetLesson();
            }
        }, 500);
    }
}

function updateLessonButtonsWithTrophies() {
    document.querySelectorAll('.lesson-btn').forEach(btn => {
        const type = btn.dataset.type;
        const index = btn.dataset.index;
        const lessonKey = `${type}-${index}`;
        if (completedLessons.has(lessonKey)) {
            const pattern = btn.textContent.replace(' 🏆', '');
            btn.innerHTML = `${pattern} 🏆`;
        }
    });
}

function updateLessonDisplay() {
    const prompt = document.getElementById('lesson-prompt');
    const fullText = generateLessonText(currentPattern, 10);
    const typedLength = patternIndex;
    
    let html = '';
    for (let i = 0; i < fullText.length; i++) {
        if (i < typedLength) {
            html += `<span class="correct">${fullText[i]}</span>`;
        } else if (i === typedLength) {
            html += `<span class="current">${fullText[i]}</span>`;
        } else {
            html += fullText[i];
        }
    }
    prompt.innerHTML = html;
}

function updateLessonStats() {
    const accuracy = lessonTotal > 0 ? Math.round(((lessonTotal - lessonErrors) / lessonTotal) * 100) : 0;
    document.getElementById('accuracy').textContent = accuracy + '%';
    document.getElementById('errors').textContent = lessonErrors;
}

function resetLesson() {
    patternIndex = 0;
    lessonErrors = 0;
    lessonTotal = 0;
    document.getElementById('lesson-input').value = '';
    document.getElementById('accuracy').textContent = '0%';
    document.getElementById('errors').textContent = '0';
    updateLessonDisplay();
    document.getElementById('lesson-input').focus();
}

async function selectDifficulty(diff) {
    selectedDifficulty = diff;
    document.querySelectorAll('.difficulty-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.difficulty-btn[data-diff="${diff}"]`).classList.add('active');

    const textsForLang = allTexts[selectedLanguage];
    if (!textsForLang) return;
    
    const textsForDiff = textsForLang[diff];
    if (!textsForDiff) return;
    
    currentTextIndex = Math.floor(Math.random() * textsForDiff.length);
    textContent = textsForDiff[currentTextIndex];
    
    textIndex = 0;
    textErrors = 0;
    textTotal = 0;
    textActive = false;

    document.getElementById('text-display').innerHTML = `<span class="current">${textContent[0]}</span>${textContent.slice(1)}`;
    document.getElementById('text-input').value = '';
    document.getElementById('text-area').style.display = 'block';
    document.getElementById('results-area').style.display = 'none';
    document.getElementById('text-input').focus();

    highlightKeys(textContent[0]);
}

function selectTrainMode(mode) {
    selectedTrainMode = mode;
    
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
        document.getElementById('timer-display').style.display = 'none';
    }
    
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.mode-btn[data-train="${mode}"]`).classList.add('active');

    const timerOptions = document.getElementById('timer-options');
    if (mode === 'timer') {
        timerOptions.style.display = 'block';
    } else {
        timerOptions.style.display = 'none';
    }

    if (selectedDifficulty) {
        selectDifficulty(selectedDifficulty);
    }
}

function selectDuration(time) {
    selectedDuration = time;
    document.querySelectorAll('.duration-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.duration-btn[data-time="${time}"]`).classList.add('active');

    if (selectedDifficulty) {
        selectDifficulty(selectedDifficulty);
    }
}

const ACCENT_MAP = {
    'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
    'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
    'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
    'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
    'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
    'ñ': 'n', 'ç': 'c', 'ÿ': 'y'
};

function normalizeAccents(char) {
    return ACCENT_MAP[char.toLowerCase()] || char.toLowerCase();
}

function charsMatch(typedChar, expectedChar) {
    // ENGLISH → case-sensitive
    if (selectedLanguage === 'english') {
        return typedChar === expectedChar;
    }

    // FR & ES → case-sensitive but accent-insensitive

    // First enforce case match
    const sameCase =
        (typedChar === typedChar.toUpperCase() && expectedChar === expectedChar.toUpperCase()) ||
        (typedChar === typedChar.toLowerCase() && expectedChar === expectedChar.toLowerCase());

    if (!sameCase) return false;

    // Then compare normalized accents
    return normalizeAccents(typedChar) === normalizeAccents(expectedChar);
}

function handleTextInput(e) {
    const input = e.target;
    const value = input.value;

    if (!textActive && value.length > 0) {
        textActive = true;
        startTime = Date.now();
        if (selectedTrainMode === 'timer') {
            startTimer();
        }
    }

    if (value.length > 0) {
        const lastChar = value[value.length - 1];
        textTotal++;

        if (charsMatch(lastChar, textContent[textIndex])) {
            textIndex++;
            input.classList.remove('error');
            input.classList.add('correct');
            setTimeout(() => input.classList.remove('correct'), 100);

            if (textIndex < textContent.length) {
                updateTextDisplay();
                highlightKeys(textContent[textIndex]);
            } else {
                if (selectedTrainMode === 'timer') {
                    textIndex = 0;
                    updateTextDisplay();
                    highlightKeys(textContent[textIndex]);
                } else {
                    finishText();
                }
            }
        } else {
            textErrors++;
            const expectedChar = textContent[textIndex];
            errorLetters[expectedChar] = (errorLetters[expectedChar] || 0) + 1;
            saveToStorage('error_letters', errorLetters);
            playSound('error');
            input.classList.add('error');
            setTimeout(() => input.classList.remove('error'), 300);
        }
    }

    input.value = '';
    updateTextStats();
}

function updateTextDisplay() {
    const display = document.getElementById('text-display');
    let html = '';
    
    for (let i = 0; i < textContent.length; i++) {
        if (i < textIndex) {
            html += `<span class="correct">${textContent[i]}</span>`;
        } else if (i === textIndex) {
            html += `<span class="current">${textContent[i]}</span>`;
        } else {
            html += textContent[i];
        }
    }
    display.innerHTML = html;
}

function updateTextStats() {
    const elapsed = startTime ? (Date.now() - startTime) / 1000 / 60 : 0;
    const wpm = elapsed > 0 ? Math.round(textIndex / 5 / elapsed) : 0;
    const accuracy = textTotal > 0 ? Math.round(((textTotal - textErrors) / textTotal) * 100) : 0;

    document.getElementById('wpm').textContent = wpm;
    document.getElementById('text-accuracy').textContent = accuracy + '%';
    document.getElementById('text-errors').textContent = textErrors;
}

function startTimer() {
    timeRemaining = selectedDuration * 60;
    document.getElementById('timer-display').style.display = 'block';
    updateTimerDisplay();

    timerInterval = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();

        if (timeRemaining <= 0) {
            finishText();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(timeRemaining / 60);
    const seconds = timeRemaining % 60;
    document.getElementById('timer').textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

function finishText() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    const elapsed = startTime ? (Date.now() - startTime) / 1000 / 60 : 0;
    const wpm = elapsed > 0 ? Math.round(textIndex / 5 / elapsed) : 0;
    const accuracy = textTotal > 0 ? Math.round(((textTotal - textErrors) / textTotal) * 100) : 0;
    const words = textContent.slice(0, textIndex).split(/\s+/).filter(w => w.length > 0).length;
    const chars = textIndex;

    const result = {
        type: 'text',
        difficulty: selectedDifficulty,
        language: selectedLanguage,
        mode: selectedTrainMode,
        duration: selectedTrainMode === 'timer' ? selectedDuration : null,
        wpm: wpm,
        accuracy: accuracy,
        errors: textErrors,
        chars: chars,
        words: words,
        timestamp: new Date().toISOString()
    };
    sessionResults.push(result);
    saveToStorage('session_results', sessionResults);

    playSound('success');

    document.getElementById('result-wpm').textContent = wpm;
    document.getElementById('result-accuracy').textContent = accuracy + '%';
    document.getElementById('result-errors').textContent = textErrors;
    document.getElementById('result-chars').textContent = chars;
    document.getElementById('result-words').textContent = words;

    document.getElementById('text-area').style.display = 'none';
    document.getElementById('timer-display').style.display = 'none';
    document.getElementById('results-area').style.display = 'block';
}

function resetText() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }

    textIndex = 0;
    textErrors = 0;
    textTotal = 0;
    textActive = false;
    startTime = null;

    document.getElementById('text-input').value = '';
    document.getElementById('timer-display').style.display = 'none';
    document.getElementById('wpm').textContent = '0';
    document.getElementById('text-accuracy').textContent = '0%';
    document.getElementById('text-errors').textContent = '0';

    if (selectedDifficulty && textContent) {
        document.getElementById('text-display').innerHTML = `<span class="current">${textContent[0]}</span>${textContent.slice(1)}`;
        highlightKeys(textContent[0]);
    }

    document.getElementById('text-input').focus();
}

function highlightHomeRow() {
    const homeRowKeys = window.HOME_ROW_DVORAK || ['a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's'];
    homeRowKeys.forEach(dvorakKey => {
        const qwertyKey = dvorakToQwerty(dvorakKey);
        const keyElement = document.querySelector(`.key[data-key="${qwertyKey}"]`);
        if (keyElement) {
            keyElement.classList.add('home-row');
        }
    });
}

function handleKeyDown(e) {
    const typedChar = e.key.toLowerCase();
    const qwertyPos = dvorakToQwerty(typedChar);
    const keyElement = document.querySelector(`.key[data-key="${qwertyPos}"]`);
    if (keyElement) {
        keyElement.classList.add('pressed');
    }
}

function handleKeyUp(e) {
    const typedChar = e.key.toLowerCase();
    const qwertyPos = dvorakToQwerty(typedChar);
    const keyElement = document.querySelector(`.key[data-key="${qwertyPos}"]`);
    if (keyElement) {
        keyElement.classList.remove('pressed');
    }
}

soundsEnabled = loadFromStorage('sounds_enabled', true);

document.addEventListener('DOMContentLoaded', init);
