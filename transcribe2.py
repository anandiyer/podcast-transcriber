import requests
import whisper
import urllib.parse
import os
from ollama import Client

def download_audio(url):
    if "listennotes.com" not in url:
        raise ValueError("The URL must be from listennotes.com")

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to download audio: {e}")

    parsed_url = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed_url.path)

    if not filename:
        filename = "downloaded_audio.mp3"

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

    try:
        model = whisper.load_model("base")
    except Exception as e:
        raise RuntimeError(f"Failed to load Whisper model: {e}")

    try:
        result = model.transcribe(audio_file)
    except Exception as e:
        raise RuntimeError(f"Failed to transcribe audio: {e}")

    full_text = result["text"]

    try:
        summary = generate_summary_with_llama(full_text)
    except Exception as e:
        raise RuntimeError(f"Failed to generate summary: {e}")

    return full_text, summary

def generate_summary_with_llama(text):
    client = Client(host='http://localhost:11434')
    
    prompt = f"""Please provide a concise summary of the following text. Focus on the key points and main ideas:

{text}

Summary:"""
    
    try:
        response = client.generate(
            model='llama3.2',
            prompt=prompt,
            stream=False
        )
        return response['response'].strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate summary with Llama: {e}")

def main():
    url = input("Enter the listennotes.com URL of the audio file: ").strip()

    if not url:
        print("Error: URL cannot be empty.")
        return

    audio_file = None

    try:
        audio_file = download_audio(url)
        print(f"Audio file downloaded: {audio_file}")

        full_text, summary = transcribe_and_summarize(audio_file)

        print("\nFull Transcription:")
        print(full_text)

        print("\nSummary:")
        print(summary)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        if audio_file and os.path.exists(audio_file):
            try:
                os.remove(audio_file)
                print(f"\nCleaned up: {audio_file} removed.")
            except Exception as e:
                print(f"Failed to remove audio file: {e}")

if __name__ == "__main__":
    main()
