#!/bin/bash

pkill -f "flask run" 2>/dev/null || pkill -f "python.*app.py" 2>/dev/null || true

echo "Dvorak Typing Trainer has been stopped."
