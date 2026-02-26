#!/usr/bin/env python3
"""
Entry point for the Dvorak Typing Trainer application.
Works on Linux, macOS, and Windows.
"""

import os
import sys

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def main():
    """Run the Flask application."""
    import app
    
    # Get port from environment or use default
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    
    print(f"Starting Dvorak Typing Trainer...")
    print(f"Server running at http://{host.replace('0.0.0.0', 'localhost')}:{port}")
    print(f"Press Ctrl+C to stop the server")
    print()
    
    app.app.run(host=host, port=port, debug=True)


if __name__ == '__main__':
    main()
