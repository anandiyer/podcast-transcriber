import requests
import whisper
import urllib.parse
import os
import sys

def download_audio(url):
    # Ensure the URL is from listennotes.com
    if "listennotes.com" not in url:
        raise ValueError("The URL must be from listennotes.com")

    # Send a GET request to the URL
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download audio: {e}")

    # Extract the filename from the URL
    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # If filename is empty, use a default name
    if not filename:
        filename = "downloaded_audio.mp3"

    # Save the audio file
    try:
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    except IOError as e:
        raise RuntimeError(f"Failed to save audio file: {e}")

    return filename

def transcribe_and_summarize(audio_file):
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    # Load the Whisper model
    try:
        model = whisper.load_model("base")
    except Exception as e:
        raise RuntimeError(f"Failed to load Whisper model: {e}")

    # Transcribe the audio
    try:
        result = model.transcribe(audio_file)
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe audio: {e}")

    # Get the full transcription
    full_text = result["text"]

    # Create a simple summary (first 100 words)
    summary = ' '.join(full_text.split()[:100]) + '...'

    return full_text, summary

def main():
    # Get the URL from user input
    url = input("Enter the listennotes.com URL of the audio file: ").strip()

    if not url:
        print("Error: URL cannot be empty.")
        return

    audio_file = None

    try:
        # Download the audio file
        audio_file = download_audio(url)
        print(f"Audio file downloaded: {audio_file}")

        # Transcribe and summarize the audio
        full_text, summary = transcribe_and_summarize(audio_file)

        print("\nFull Transcription:")
        print(full_text)

        # print("\nSummary (first 100 words):")
        # print(summary)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Clean up: remove the downloaded audio file
        if audio_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
                print(f"\nCleaned up: {audio_file} removed.")
            except Exception as e:
                print(f"Failed to remove audio file: {e}")

if __name__ == "__main__":
    main()
