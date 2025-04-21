# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai

# Replace with your API key
aai.settings.api_key = ""

# You can also transcribe a local file by passing in a file path
FILE_URL = 'audio/1.m4a'

# You can set additional parameters for the transcription
config = aai.TranscriptionConfig(
    speech_model=aai.SpeechModel.best,
    auto_chapters=True,
    language_detection=True
)

transcriber = aai.Transcriber(config=config)
transcript = transcriber.transcribe(FILE_URL)

if transcript.status == aai.TranscriptStatus.error:
    print(transcript.error)
else:
    print(transcript.text)
    print()
    for chapter in transcript.chapters:
        print(f"{chapter.start}-{chapter.end}: {chapter.headline}")

