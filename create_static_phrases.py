# create_static_phrases.py
from gtts import gTTS
import os

os.makedirs("responses", exist_ok=True)

phrases = {
    "your_name_is": "आपका नाम",
    "you_want_loan": "है। आपने ... रुपये का लोन ...",
    "tenure_is": "महीनों में चुकाना चाहेंगे। आप",
    "employment_is": "हैं। आपकी ब्याज दर"
}

for filename, text in phrases.items():
    tts = gTTS(text=text, lang="hi")
    tts.save(f"responses/{filename}.mp3")
    print(f"Created {filename}.mp3")
