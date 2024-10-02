#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null
then
    echo "ffmpeg is not installed. Please install it before continuing."
    echo "On Ubuntu or Debian: sudo apt update && sudo apt install ffmpeg"
    echo "On MacOS with Homebrew: brew install ffmpeg"
    exit 1
fi

# Create and activate a virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

echo "Setup complete. You can now run the script."
