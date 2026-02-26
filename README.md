# Dvorak Typing Trainer
Support development: [Ko-Fi](https://ko-fi.com/clicolourize)

A web-based typing trainer for learning the Dvorak keyboard layout. Practice typing in English, French, and Spanish with visual keyboard feedback, lessons, and statistics tracking.

## Features

- Visual Dvorak keyboard with key highlighting
- 2-letter, 4-letter, and Common Words lessons with achievements
- Text training in English, French, and Spanish with multiple difficulty levels
- Full text mode and timer mode (1/2/3/5 minutes)
- Sound effects for errors and successes
- Statistics dashboard with persistent progress (localStorage)
- Settings menu with reset option

## Folder Structure

```
dvorak-typing-trainer/
├── app/
│   ├── __init__.py          # Flask app factory (optional)
│   ├── app.py               # Main Flask application
│   ├── static/
│   │   ├── script.js        # Frontend JavaScript
│   │   └── style.css        # Frontend styles
│   └── templates/
│       └── index.html       # Main HTML template
├── texts/
│   ├── __init__.py
│   ├── french.py            # French text content
│   └── spanish.py           # Spanish text content
├── tests/                   # Test files (optional)
├── venv/                    # Virtual environment (auto-generated)
├── .gitignore
├── requirements.txt
├── README.md
├── run.py                   # Entry point to run the app
├── start.bat                # Windows start script
├── stop.bat                 # Windows stop script
├── render.yaml              # Render deployment configuration
└── SPEC.md                  # Project specification
```

## Prerequisites

- Python 3.8 or higher
- Web browser (Chrome, Firefox, Safari, Edge)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/dvorak-typing-trainer.git
cd dvorak-typing-trainer
```

### 2. Create Virtual Environment

**Linux/MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Locally

### Linux/MacOS

```bash
# Method 1: Using run.py
python run.py

# Method 2: Directly with Flask
export FLASK_APP=app/app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### Windows

```cmd
# Using the batch file
start.bat
```

Or manually:
```cmd
set FLASK_APP=app\app.py
set FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

The application will be available at: **http://localhost:5000**

## Stopping the Application

### Linux/MacOS

Press `Ctrl+C` in the terminal where Flask is running.

### Windows

Run the stop script or press `Ctrl+C` in the command prompt.

## Deployment to Render

### Option 1: Using render.yaml (Recommended)

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Use the following settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app.app:app`
4. Add the following environment variable:
   - `PYTHON_VERSION`: `3.9` (or your preferred version)

### Option 2: Manual Deployment

1. Create a `Procfile` (see below) in the root directory
2. Push to GitHub
3. Connect repository to Render
4. Render will automatically detect the Python service

### Procfile Content

```
web: gunicorn app.app:app
```

**Note:** You'll need to add `gunicorn` to `requirements.txt` for production deployment:
```
flask==3.0.0
gunicorn>=21.0.0
```

## Usage

1. **Select Language**: Choose English, French, or Spanish from the top menu
2. **Choose Mode**: Select Lessons or Text Training
3. **Select Difficulty**: Easy, Medium, or Hard
4. **Choose Timer Mode**: Full text or timed (1/2/3/5 minutes)
5. **Start Typing**: Begin typing the displayed text
6. **View Statistics**: Check your progress in the Statistics tab

### Typing Rules

- **English**: Case-sensitive (A ≠ a)
- **French**: Case-sensitive, accent-insensitive (á = a, é = e)
- **Spanish**: Case-sensitive, accent-insensitive (á = a, é = e)

## Troubleshooting

### Port Already in Use

If port 5000 is already in use, specify a different port:

```bash
# Linux/MacOS
flask run --port=5001

# Windows
set FLASK_RUN_PORT=5001
flask run
```

### Virtual Environment Issues

If you have issues activating the virtual environment:

```bash
# Linux/MacOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

### Database/Storage Issues

The app uses browser localStorage for data persistence. Clear your browser's localStorage if you experience issues:

1. Open Developer Tools (F12)
2. Go to Application > Storage > Local Storage
3. Right-click and clear the entries

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
6. Report issues here: [GitHub Issues](https://github.com/clicolourize/dvorak-typing-trainer/issues)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Dvorak keyboard layout information
- Flask web framework
- All contributors and testers
