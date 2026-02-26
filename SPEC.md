# Dvorak Typing Trainer - Specification

## Project Overview
- **Project name**: Dvorak Typing Trainer
- **Type**: Web application (Flask + HTML/CSS/JS)
- **Core functionality**: Interactive typing trainer teaching Dvorak keyboard layout with visual keyboard feedback, lessons, and timed exercises
- **Target users**: People wanting to learn the Dvorak keyboard layout

---

## Technical Stack
- **Backend**: Python Flask (lightweight web framework)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **No database**: All data stored in-memory
- **Port**: 5000 (default Flask)

---

## UI/UX Specification

### Layout Structure
```
+------------------------------------------+
|              HEADER                       |
|   "Dvorak Typing Trainer" + Mode Tabs    |
+------------------------------------------+
|                                          |
|           MAIN CONTENT AREA              |
|   (Lessons / Text Training / Results)    |
|                                          |
+------------------------------------------+
|           DVORAK KEYBOARD                |
|    (Visual keyboard with highlighting)  |
+------------------------------------------+
```

### Visual Design
- **Primary color**: #1a1a2e (dark navy background)
- **Secondary color**: #16213e (slightly lighter panels)
- **Accent color**: #0f3460 (buttons, highlights)
- **Highlight color**: #e94560 (active keys - bright pink/red)
- **Success color**: #4ecca3 (correct typing)
- **Error color**: #ff6b6b (mistakes)
- **Text color**: #eaeaea (light gray)
- **Font**: "JetBrains Mono" for typing area, "Poppins" for UI

### Keyboard Display
- Standard QWERTY physical layout visually re-mapped to Dvorak
- Keys light up in pink/red (#e94560) when being practiced
- Current target key(s) have pulsing animation
- Home row keys (a, o, e, u, i, d, h, t, n, s) subtly highlighted as reference

---

## Functionality Specification

### Mode 1: Lessons
**Purpose**: Teach keys incrementally through pattern practice

#### 2-Letter Lessons (20 lessons)
- Focus on 10 key pairs, teaching home row first
- Pattern format: repeat 2 letters 10 times (e.g., "etet etet etet...")
- Progression:
  1. ao (home row left hand)
  2. ,. (comma, period - punctuation)
  3. eo (home row mix)
  4. uu 
  5. ie
  6. id
  7. ht
  8. tn
  9. sn
  10. dh
  ...and more pairs covering all keys

#### 4-Letter Lessons (26 lessons - A to Z)
- Each lesson focuses on a specific letter combination
- Format: 4-letter pattern repeated (e.g., "etuh etuh etuh...")
- Patterns: et, an, ic, um, or, etc.

#### Lesson Behavior
- Show current pattern prominently
- User types the pattern
- Correct: green flash, advance
- Incorrect: red flash, error sound (optional), must retry
- Show accuracy percentage
- Progress to next lesson automatically on 90%+ accuracy

### Mode 2: Text Training
**Purpose**: Practice typing real text

#### Text Difficulty Levels
1. **Easy**: Short sentences, common words, ~50 words
2. **Medium**: Medium sentences, some uncommon words, ~100 words  
3. **Hard**: Longer sentences, all letters, ~150 words

#### Training Modes
1. **Full Text Mode**:
   - Display entire text
   - User types until completion or gives up
   - Show WPM, accuracy, errors at end

2. **Timer Mode**:
   - Select duration: 1, 2, 3, or 5 minutes
   - Countdown timer displayed
   - Type as much as possible in time limit
   - Show: characters typed, words typed, WPM, accuracy

### Sample Texts (Silly Stories)

#### Easy (50 words)
"The cat sat on a hat. It was a fat cat. The cat ran to a pan. It can hop. Hop, cat, hop!"

#### Medium (100 words)
"A funny bunny went to the moon. The moon was made of cheese! The bunny ate and ate. Then the bunny ran to a rocket. The rocket went zip-zap! Now the bunny is home. Home is where the carrot is. Eat, bunny, eat!"

#### Hard (150 words)
"Peter Piper picked a peck of pickled peppers. A peck of pickled peppers Peter Piper picked. Where's the peck of pickled peppers Peter Piper picked? Sally sells seashells by the seashore. She sells yew trees too. The quick brown fox jumps over the lazy dog. How vexingly quick daft zebras jump!"

---

## Keyboard Mapping (Dvorak)
```
Row 1 (number row):  ' " , . p y f g c r l / = \ 
Row 2 (top letters): o e u i d h t n s - 
Row 3 (home):        a q j k x b m w v z
Row 4 (space):       (space)
```

### Key Visual Layout
```
`  1  2  3  4  5  6  7  8  9  0  -  =  Backspace
 '  ,  .  p  y  f  g  c  r  l  /  \     
   o  e  u  i  d  h  t  n  s  -        
  a  q  j  k  x  b  m  w  v  z         
                         (space)
```

---

## File Structure
```
/home/user/Scripts/speedtyping/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── static/
│   ├── style.css        # Styles
│   └── script.js        # Frontend logic
├── templates/
│   └── index.html      # Main HTML template
├── run.sh              # Start script with venv
└── stop.sh             # Stop script
```

---

## Scripts Specification

### run.sh
```bash
#!/bin/bash
# Creates venv if not exists, installs deps, starts app, opens browser

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate venv and install deps
source venv/bin/activate
pip install -r requirements.txt

# Start Flask in detached mode
flask run --host=0.0.0.0 --port=5000 &

# Wait a moment
sleep 2

# Open browser
xdg-open http://localhost:5000 &
```

### stop.sh
```bash
#!/bin/bash
# Finds and kills Flask process

pkill -f "flask run" || true
# Or use pkill -f "python.*app.py"
```

---

## Acceptance Criteria

1. Dvorak keyboard displays at bottom of screen in QWERTY physical layout
2. Keys highlight in pink/red when being practiced in lessons
3. 20+ 2-letter lessons covering key pairs
4. 26+ 4-letter lessons (one per letter combination focus)
5. Text training with Easy/Medium/Hard difficulty
6. Full text mode: type until completion
7. Timer mode: 1/2/3/5 minute options
8. WPM and accuracy displayed after exercises
9. run.sh creates venv, installs deps, opens browser
10. stop.sh terminates application
