from flask import Flask, request, send_file
from twilio.twiml.voice_response import VoiceResponse, Gather
import json
from utils import log_call
from generate_summary import create_summary
import os
import pandas as pd

app = Flask(__name__)

with open("kb.json", "r", encoding="utf-8") as f:
    KB = json.load(f)

sessions = {}
EXCEL_LOG = "call_logs.xlsx"

yes_words = ["हाँ", "haan", "ha", "haanji", "sahi hai"]
no_words = ["नहीं", "no", "nahi", "nahi chahiye", "ना", "नहीं चाहिए"]

def get_audio(filename):
    return f"responses/{filename}.mp3"

def log_to_excel(data):
    df = pd.DataFrame([data])
    if os.path.exists(EXCEL_LOG):
        existing = pd.read_excel(EXCEL_LOG)
        df = pd.concat([existing, df], ignore_index=True)
    df.to_excel(EXCEL_LOG, index=False)

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

    if any(word in speech for word in no_words):
        resp.play(url=request.url_root + "audio/bye.mp3")
        resp.hangup()
        return str(resp)

    gather = Gather(input="speech", action="/name", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_name.mp3")
    resp.append(gather)
    return str(resp)

@app.route("/name", methods=["POST"])
def get_name():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/voice")
        return str(resp)
    sessions[call_sid]["name"] = speech

    gather = Gather(input="speech", action="/amount", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_amount.mp3")
    resp.append(gather)
    return str(resp)

@app.route("/amount", methods=["POST"])
def get_amount():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/name")
        return str(resp)

    try:
        amount_val = int(speech.replace(",", "").replace("₹",""))
    except:
        amount_val = speech

    # Loan limit check
    if isinstance(amount_val, int) and amount_val > 500000:
        gather = Gather(input="speech", action="/amount", language="hi-IN", speechTimeout="auto")
        gather.play(url=request.url_root + "audio/loan_limit.mp3")
        resp.append(gather)
        return str(resp)

    sessions[call_sid]["amount"] = str(amount_val)

    gather = Gather(input="speech", action="/tenure", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_tenure.mp3")
    resp.append(gather)
    return str(resp)

@app.route("/tenure", methods=["POST"])
def get_tenure():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/amount")
        return str(resp)
    sessions[call_sid]["tenure"] = speech

    gather = Gather(input="speech", action="/confirm_info", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/confirm_info.mp3")
    resp.append(gather)
    return str(resp)

@app.route("/confirm_info", methods=["POST"])
def confirm_info():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip().lower()
    resp = VoiceResponse()

    if any(word in speech for word in no_words):
        resp.redirect("/name")
        return str(resp)

    gather = Gather(input="speech", action="/employment", language="hi-IN", speechTimeout="auto")
    gather.play(url=request.url_root + "audio/ask_employment.mp3")
    resp.append(gather)
    return str(resp)

@app.route("/employment", methods=["POST"])
def employment():
    call_sid = request.form.get("CallSid")
    speech = request.form.get("SpeechResult", "").strip()
    resp = VoiceResponse()
    if not speech:
        resp.redirect("/confirm_info")
        return str(resp)

    sessions[call_sid]["employment"] = speech
    tenure = sessions[call_sid]["tenure"]
    rate = KB.get(tenure, 11.0)
    sessions[call_sid]["rate"] = rate

    create_summary(
        sessions[call_sid]["name"],
        sessions[call_sid]["amount"],
        sessions[call_sid]["tenure"],
        sessions[call_sid]["employment"],
        sessions[call_sid]["rate"]
    )

    summary_order = [
        "your_name_is", "name",
        "you_want_loan", "amount",
        "tenure_is", "tenure",
        "employment_is", "employment",
        "rate_intro", "rate",
        "thank_you"
    ]

    for fname in summary_order:
        path = f"responses/{fname}.mp3"
        if os.path.exists(path):
            resp.play(url=request.url_root + f"audio/{fname}.mp3")

    log_data = {
        "CallSid": call_sid,
        "From": request.form.get("From"),
        "Name": sessions[call_sid]["name"],
        "Amount": sessions[call_sid]["amount"],
        "Tenure": sessions[call_sid]["tenure"],
        "Rate": sessions[call_sid]["rate"],
        "Employment": sessions[call_sid]["employment"],
        "Status": "Confirmed"
    }
    log_to_excel(log_data)

    resp.hangup()
    return str(resp)

@app.route("/audio/<filename>")
def audio(filename):
    return send_file(f"responses/{filename}")

@app.route("/bye", methods=["POST"])
def bye():
    resp = VoiceResponse()
    resp.play(url=request.url_root + "audio/bye.mp3")
    resp.hangup()
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
