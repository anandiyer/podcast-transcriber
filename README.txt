Audio Transcription and Summarization Tool

This script downloads an audio file from ListenNotes, transcribes it using OpenAI's Whisper model, and provides a brief summary.

Features:
- Download Audio: Fetches audio files directly from ListenNotes.
- Transcription: Transcribes audio using the Whisper model.
- Summarization: Generates a summary from the first 100 words of the transcription.
- Error Handling: Robust handling of network and file errors.

Requirements:
- Python 3.x
- requests library
- whisper library

Installation:
1. Clone the repository:
   git clone https://github.com/anandiyer/podcast-transcriber.git
   cd podcast-transcriber

2. Install required packages:
   pip install requests whisper

Usage:
1. Run the script:
   python podcast-transcriber.py

2. Enter the ListenNotes URL when prompted.

Example:
Enter the listennotes.com URL of the audio file: <URL>

Notes:
- Ensure the URL is from listennotes.com.
- The downloaded audio file is automatically deleted after processing.

Contributing:
Feel free to submit issues or pull requests for improvements!

License:
This project is licensed under the MIT License.
