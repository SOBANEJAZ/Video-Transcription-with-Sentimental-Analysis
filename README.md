# Audio Transcription and Sentiment Analysis

## Overview

This GitHub repository contains a script that uses OpenAI’s Whisper model for transcription and TextBlob for sentiment analysis. The script performs the following tasks:

- **Transcription**: Transcribes audio from a video file, extracting words with their corresponding timestamps using the Whisper model. The transcriptions are saved in a JSON file with word-level timestamp information.

- **Sentence Formation**: Processes the transcriptions to reconstruct sentences based on punctuation marks that typically end sentences.

- **Sentiment Analysis**: Analyzes each reconstructed sentence for sentiment using TextBlob. Sentiment is categorized as positive, negative, or neutral based on polarity.

- **Output**: Saves the results, including each sentence with its timestamp and sentiment score, in a JSON file.

>  Given the computational intensity of this task, here is the link to the Google Colab notebook to test the code in real time:
> [Google Colab Notebook](https://colab.research.google.com/drive/1nswmb47_jL-2DayXuV5qlEUOUCD5n9y4?usp=sharing) 

## Setup Instructions

### Step 1: Install Dependencies
Ensure Python is installed on your system, then install the necessary dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 2: Select the Whisper Model
Whisper models are available in various sizes. Depending on your needs, download the appropriate model. You can specify the model in the code by changing the model name:
```bash
model_size = "base" # Change "base" to "large", "medium", "small", or "tiny" as per your requirements
```
Depending on your available resources and the desired balance between speed and accuracy. The table below explains the trade-offs:

| Model Size | Parameters | Accuracy       | Speed   | Resource Usage |
|------------|------------|----------------|---------|----------------|
| Tiny       | Smallest   | Lowest         | Fastest | Lowest         |
| Base       | Small      | Low to Medium  | Fast    | Low            |
| Small      | Medium     | Medium         | Moderate| Moderate       |
| Medium     | Large      | High           | Slower  | High           |
| Large      | Largest    | Highest        | Slowest | Very High      |

### Step 3: Change the Path of the Audio File
In the provided code, you will need to specify the path of the audio file you want to transcribe. Replace the placeholder path with the actual path to your audio file:
```bash
path_to_file = "path_to_file.mp4"
```
