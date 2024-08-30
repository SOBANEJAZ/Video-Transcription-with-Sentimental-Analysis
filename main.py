from textblob import TextBlob
import whisper
import json

# 
path_to_file = "path_to_file.mp4"
# path_to_file = "/content/drive/MyDrive/input.mp4"


# Define the model size
model_size = "base"

# Load the Whisper model
model = whisper.load_model(model_size)

# Transcribe the audio file
result = model.transcribe(path_to_file, word_timestamps=True)

# Extract the words and their timestamps
words_with_timestamps = []
for segment in result["segments"]:
    for word in segment["words"]:
        words_with_timestamps.append({"word": word["word"], "timestamp": word["start"]})

# Save the result as a JSON file
import json

with open("transcription_with_timestamps.json", "w") as f:
    json.dump(words_with_timestamps, f, indent=4)


# Example JSON file with words and timestamps
with open("transcription_with_timestamps.json", "r") as f:
    words_with_timestamps = json.load(f)

sentences = []
current_sentence = {"sentence": "", "timestamp": 0}

# Define punctuation that marks the end of a sentence
sentence_endings = [".", "!", "?"]

for word_info in words_with_timestamps:
    word = word_info["word"]
    if current_sentence["sentence"] == "":
        current_sentence["timestamp"] = word_info["timestamp"]

    current_sentence["sentence"] += word + " "

    if any(word.endswith(punct) for punct in sentence_endings):
        # Trim the last space and add the sentence to the list
        current_sentence["sentence"] = current_sentence["sentence"].strip()
        sentences.append(current_sentence)
        current_sentence = {"sentence": "", "timestamp": 0}

# Analyze sentiment and rate
analyzed_sentences = []
for sentence_info in sentences:
    sentence_text = sentence_info["sentence"]
    blob = TextBlob(sentence_text)
    polarity = blob.sentiment.polarity

    # Categorize the sentiment
    if polarity > 0:
        sentiment = 1  # Positive
    elif polarity < 0:
        sentiment = -1  # Negative
    else:
        sentiment = 0  # Neutral

    analyzed_sentences.append(
        {
            "sentence": sentence_text,
            "timestamp": sentence_info["timestamp"],
            "sentiment": sentiment,
        }
    )

# Save the result as a JSON file
with open("sentiment_analysis.json", "w") as f:
    json.dump(analyzed_sentences, f, indent=4)
