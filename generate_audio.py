from gtts import gTTS
import os

os.makedirs("responses", exist_ok=True)

texts = {
    "intro": "नमस्ते, मैं एक्स वाई ज़ेड बैंक से बोल रहा हूँ। आपके लिए 5 लाख रुपये तक का प्री-अप्रूव्ड लोन उपलब्ध है। क्या आप आगे बढ़ना चाहेंगे?",
    "bye": "धन्यवाद, आपके समय के लिए। अलविदा।",
    "ask_name": "कृपया अपना नाम बताइए।",
    "ask_amount": "आप कितनी राशि लेना चाहेंगे?",
    "ask_tenure": "कृपया बताइए आप कितने महीनों में भुगतान करना चाहेंगे — 12, 24, या 36?",
    "confirm_info": "आपने नाम, राशि और अवधि दर्ज किया है। क्या यह सही है?",
    "ask_employment": "क्या आप वर्तमान में employed हैं या unemployed?",
    "interest": "आपके लोन के लिए ब्याज दर {rate} प्रतिशत वार्षिक होगी। धन्यवाद।"
}

for filename, text in texts.items():
    tts = gTTS(text=text, lang="hi")
    tts.save(f"responses/{filename}.mp3")

print("All audio files generated in responses/")
