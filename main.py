import json
import os
import speech_recognition as sr
from pydub import AudioSegment
from textblob import TextBlob
from tqdm import tqdm
import moviepy.editor as mp
import nltk
from nltk.tokenize import sent_tokenize


def download_nltk_data():
    try:
        nltk.data.find("tokenizers/punkt")
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        print("Downloading necessary NLTK data...")
        nltk.download("punkt", quiet=True)
        nltk.download("punkt_tab", quiet=True)


# Call this function at the start of the script
download_nltk_data()


def extract_audio_from_video(video_file):
    # Extract audio from video
    video = mp.VideoFileClip(video_file)
    audio = video.audio
    audio_file = "temp_audio.wav"
    audio.write_audiofile(audio_file)
    return audio_file


def transcribe_audio(audio_file):
    # Initialize recognizer
    r = sr.Recognizer()

    # Load audio file
    audio = AudioSegment.from_wav(audio_file)

    # Split audio into chunks for processing
    chunk_length_ms = 30000  # 30 seconds
    chunks = [
        audio[i : i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)
    ]

    transcription = []

    for i, chunk in enumerate(tqdm(chunks)):
        # Export chunk to a temporary file
        chunk.export(f"temp_chunk_{i}.wav", format="wav")

        # Transcribe chunk
        with sr.AudioFile(f"temp_chunk_{i}.wav") as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data, show_all=True)
                if text and "alternative" in text:
                    for alt in text["alternative"]:
                        words = alt["transcript"].split()
                        for word in words:
                            timestamp = (
                                i * chunk_length_ms / 1000 + len(transcription) * 0.5
                            )  # Rough estimate
                            transcription.append(
                                {"word": word, "timestamp": format_timestamp(timestamp)}
                            )
            except sr.UnknownValueError:
                print(f"Could not understand audio in chunk {i}")
            except sr.RequestError as e:
                print(f"Could not request results from speech recognition service; {e}")

        # Clean up temporary chunk file
        os.remove(f"temp_chunk_{i}.wav")

    return transcription


def format_timestamp(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}:{int((seconds % 1) * 1000):03d}"


def perform_sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity

    # Categorize sentiment
    if sentiment_score > 0.05:
        sentiment = "positive"
    elif sentiment_score < -0.05:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {"sentiment": sentiment, "score": sentiment_score}


def process_podcast(video_file):
    # Extract audio from video
    audio_file = extract_audio_from_video(video_file)

    # Transcribe audio
    transcription = transcribe_audio(audio_file)

    # Combine words into full text
    full_text = " ".join([item["word"] for item in transcription])

    # Split text into sentences
    sentences = sent_tokenize(full_text)

    # Perform sentiment analysis on each sentence
    analyzed_sentences = []
    current_word_index = 0

    for sentence in sentences:
        words_in_sentence = sentence.split()
        start_time = transcription[current_word_index]["timestamp"]
        end_time = transcription[current_word_index + len(words_in_sentence) - 1][
            "timestamp"
        ]

        sentiment = perform_sentiment_analysis(sentence)

        analyzed_sentences.append(
            {
                "text": sentence,
                "sentiment": sentiment["sentiment"],
                "sentiment_score": sentiment["score"],
                "start_time": start_time,
                "end_time": end_time,
            }
        )

        current_word_index += len(words_in_sentence)

    # Prepare final output
    output = {"transcription": transcription, "sentences": analyzed_sentences}

    # Save to JSON file
    output_file = os.path.splitext(video_file)[0] + "_analysis.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Transcription and analysis complete. Results saved to {output_file}")

    # Clean up temporary audio file
    os.remove(audio_file)


# Usage
if __name__ == "__main__":
    video_file = "input.mp4"
    process_podcast(video_file)
