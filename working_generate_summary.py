# generate_summary.py
from gtts import gTTS
import os

# Ensure responses folder exists
os.makedirs("responses", exist_ok=True)

# Static phrases for final summary
static_phrases = {
    "your_name_is": "आपका नाम",
    "you_want_loan": "है। आपने",
    "tenure_is": "महीनों में चुकाना चाहेंगे",
    "employment_is": "आप",
    "rate_intro": "आपकी ब्याज दर",
    "thank_you": "धन्यवाद आपका समय देने के लिए"
}

# Create static phrase MP3s if missing
for fname, text in static_phrases.items():
    path = f"responses/{fname}.mp3"
    if not os.path.exists(path):
        tts = gTTS(text=text, lang="hi")
        tts.save(path)
        print(f"Created static phrase: {fname}.mp3")

def create_summary(name, amount, tenure, employment, rate):
    """
    Saves all parts of the final summary as separate MP3s.
    app.py will play them in proper order.
    """
    # Dynamic parts as TTS
    dynamic_values = {
        "name": name,
        "amount": amount,
        "tenure": tenure,
        "employment": employment,
        "rate": str(rate)
    }

    for key, value in dynamic_values.items():
        path = f"responses/{key}.mp3"
        tts = gTTS(text=value, lang="hi")
        tts.save(path)
        print(f"Created dynamic TTS: {key}.mp3")
