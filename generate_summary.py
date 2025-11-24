from gtts import gTTS
import os

# Ensure responses folder exists
os.makedirs("responses", exist_ok=True)

# Mapping for static phrases
STATIC_PHRASES = {
    "your_name_is": "आपका नाम",
    "you_want_loan": "है। आपने",
    "tenure_is": "महीनों में चुकाना चाहेंगे।",
    "employment_is": "आप वर्तमान में",
    "rate_intro": "आपकी ब्याज दर",
    "thank_you": "धन्यवाद।"
}

# Create static phrase MP3s if missing
for key, text in STATIC_PHRASES.items():
    path = f"responses/{key}.mp3"
    if not os.path.exists(path):
        tts = gTTS(text=text, lang="hi")
        tts.save(path)

# Helper to convert numbers to Hindi words
def number_to_hindi(n):
    # Simple mapping for lakh level numbers (can expand)
    units = ["", "एक", "दो", "तीन", "चार", "पाँच", "छह", "सात", "आठ", "नौ"]
    tens = ["", "दस", "बीस", "तीस", "चालीस", "पचास", "साठ", "सत्तर", "अस्सी", "नब्बे"]
    if n >= 100000:
        lakhs = n // 100000
        remainder = n % 100000
        return f"{units[lakhs]} लाख {remainder}" if remainder else f"{units[lakhs]} लाख"
    return str(n)

def create_summary(name, amount, tenure, employment, rate):
    """Generates dynamic MP3s for the final summary"""
    # Convert amount to Hindi words
    try:
        amt = int(amount.replace(",", "").replace("₹",""))
    except:
        amt = amount
    amount_hindi = number_to_hindi(amt) if isinstance(amt, int) else amt

    # Structured dynamic phrases
    dynamic_phrases = {
        "name": name,
        "amount": f"{amount_hindi} रुपये का ऋण लिया है।",
        "tenure": f"{tenure} में चुकाना चाहेंगे।",
        "employment": "रोजगार में हैं।" if "employ" in employment.lower() else "बेरोजगार हैं।",
        "rate": f"{rate}%  है।"
    }

    # Generate dynamic MP3s
    for key, text in dynamic_phrases.items():
        path = f"responses/{key}.mp3"
        tts = gTTS(text=text, lang="hi")
        tts.save(path)
