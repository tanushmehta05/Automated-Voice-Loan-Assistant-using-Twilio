from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse, Gather
import json
from utils import log_call
from generate_summary import create_summary
import os

app = Flask(__name__)

# Load knowledge base
with open("kb.json", "r", encoding="utf-8") as f:
    KB = json.load(f)

sessions = {}

# ------------------- HELPER -------------------
def get_audio(filename):
    return f"responses/{filename}.mp3"

# ------------------- BOT FLOW -------------------
@app.route("/voice", methods=["POST"])
def voice():
    call_sid = request.form.get("CallSid")
    sessions[call_sid] = {}
    resp = VoiceResponse()

    gather = Gather(input="speech", action="/continue", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/intro.mp3")
    resp.append(gather)
    resp.redirect("/continue_retry")
    return str(resp)

@app.route("/continue_retry", methods=["POST"])
def continue_retry():
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/continue", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/intro.mp3")
    resp.append(gather)
    resp.redirect("/bye")
    return str(resp)

@app.route("/continue", methods=["POST"])
def continue_call():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip().lower()
    resp = VoiceResponse()
    no_words = ["नहीं", "no", "nahi", "nahi chahiye", "ना", "नहीं चाहिए"]

    if any(word in speech for word in no_words):
        resp.play(url=request.url_root + "audio/bye.mp3")
        resp.hangup()
        return str(resp)

    gather = Gather(input="speech", action="/name", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_name.mp3")
    resp.append(gather)
    resp.redirect("/name_retry")
    return str(resp)

@app.route("/name_retry", methods=["POST"])
def name_retry():
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/name", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_name.mp3")
    resp.append(gather)
    resp.redirect("/bye")
    return str(resp)

@app.route("/name", methods=["POST"])
def get_name():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/name_retry")
        return str(resp)
    sessions[call_sid]["name"] = speech

    gather = Gather(input="speech", action="/amount", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_amount.mp3")
    resp.append(gather)
    resp.redirect("/amount_retry")
    return str(resp)

@app.route("/amount_retry", methods=["POST"])
def amount_retry():
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/amount", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_amount.mp3")
    resp.append(gather)
    resp.redirect("/bye")
    return str(resp)

@app.route("/amount", methods=["POST"])
def get_amount():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/amount_retry")
        return str(resp)
    sessions[call_sid]["amount"] = speech

    gather = Gather(input="speech", action="/tenure", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_tenure.mp3")
    resp.append(gather)
    resp.redirect("/tenure_retry")
    return str(resp)

@app.route("/tenure_retry", methods=["POST"])
def tenure_retry():
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/tenure", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_tenure.mp3")
    resp.append(gather)
    resp.redirect("/bye")
    return str(resp)

@app.route("/tenure", methods=["POST"])
def get_tenure():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/tenure_retry")
        return str(resp)
    sessions[call_sid]["tenure"] = speech

    # Confirm info
    gather = Gather(input="speech", action="/confirm_info", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/confirm_info.mp3")
    resp.append(gather)
    resp.redirect("/confirm_retry")
    return str(resp)

@app.route("/confirm_retry", methods=["POST"])
def confirm_retry():
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/confirm_info", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/confirm_info.mp3")
    resp.append(resp)
    resp.redirect("/bye")
    return str(resp)

@app.route("/confirm_info", methods=["POST"])
def confirm_info():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip().lower()
    resp = VoiceResponse()
    no_words = ["नहीं", "no", "nahi", "nahi chahiye", "ना", "नहीं चाहिए"]
    if any(word in speech for word in no_words):
        resp.redirect("/name")  # restart name step
        return str(resp)

    gather = Gather(input="speech", action="/employment", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_employment.mp3")
    resp.append(gather)
    resp.redirect("/employment_retry")
    return str(resp)

@app.route("/employment_retry", methods=["POST"])
def employment_retry():
    resp = VoiceResponse()
    gather = Gather(input="speech", action="/employment", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_employment.mp3")
    resp.append(gather)
    resp.redirect("/bye")
    return str(resp)

@app.route("/employment", methods=["POST"])
def employment():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/employment_retry")
        return str(resp)

    sessions[call_sid]["employment"] = speech
    tenure = sessions[call_sid]["tenure"]
    rate = KB.get(tenure, 11.0)
    sessions[call_sid]["rate"] = rate

    # Generate final summary TTS MP3s
    data = sessions[call_sid]
    create_summary(
        data["name"],
        data["amount"],
        data["tenure"],
        data["employment"],
        data["rate"]
    )

    # Play final summary in proper order
    summary_order = [
        "your_name_is", "name",
        "you_want_loan", "amount",
        "tenure_is", "tenure",
        "employment_is", "employment",
        "rate_intro", "rate"
    ]
    for fname in summary_order:
        path = f"responses/{fname}.mp3"
        if os.path.exists(path):
            resp.play(url=request.url_root + f"audio/{fname}.mp3")

    # Log call
    log_call(
        call_sid,
        request.form.get("From"),
        data["name"],
        data["amount"],
        data["tenure"],
        data["rate"],
        data["employment"],
        "Confirmed"
    )

    resp.hangup()
    return str(resp)

# Serve MP3s
@app.route("/audio/<filename>")
def audio(filename):
    return send_file(f"responses/{filename}")

# Fallback hangup
@app.route("/bye", methods=["POST"])
def bye():
    resp = VoiceResponse()
    resp.play(url=request.url_root + "audio/bye.mp3")
    resp.hangup()
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
