#!/bin/bash

cd /home/user/Scripts/speedtyping

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Could not create venv, using system Python..."
        rm -rf venv
    fi
fi

if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    pip install flask 2>/dev/null || pip install --break-system-packages flask 2>/dev/null || true
else
    echo "Using system Python (flask already installed if needed)..."
fi

echo "Starting Flask application..."
python3 -m flask run --host=0.0.0.0 --port=5000 &

sleep 2

echo "Opening browser..."
xdg-open http://localhost:5000 &

echo ""
echo "============================================"
echo "Dvorak Typing Trainer is running!"
echo "Open your browser at: http://localhost:5000"
echo "============================================"
