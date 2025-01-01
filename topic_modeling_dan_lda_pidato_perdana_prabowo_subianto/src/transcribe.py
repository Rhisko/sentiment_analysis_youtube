import whisper
import csv
import os


def transcribe_audio(audio_path,video_id):
    # Check if he Audio Already transcribe
    if video_id:
        existing_files = [f for f in os.listdir("data/transcripts/") if f.__contains__(video_id)]
        if existing_files:
            print(f"File already exists: {existing_files[0]} - Skipping transcribe.")
            return video_id
        
    # Load the Whisper model
    model = whisper.load_model("small")  # Change "base" to "tiny", "small", etc., for other models

    # Transcribe the audio
    result = model.transcribe(audio_path)

    # Extract transcription text
    transcription = result["text"]
    print("Transcription completed!")

    # Define CSV output file
    csv_file = f"data/transcripts/transcription_{video_id}.csv"

    # Write transcription to a CSV file
    with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Audio File", "Transcription"])  # Header row
        writer.writerow([audio_path, transcription])     # Data row

    print(f"Transcription has been saved to '{csv_file}'")
