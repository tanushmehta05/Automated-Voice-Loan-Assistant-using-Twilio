# Twilio Loan Eligibility Voice Bot (Hindi)

This repository contains an automated Interactive Voice Response (IVR) system built using Twilio Programmable Voice, Flask, and speech recognition. The bot collects loan eligibility information through a phone call and provides a dynamically generated spoken summary in Hindi.

The system automates lead qualification by gathering user inputs such as name, requested loan amount, repayment tenure, and employment status, and then computing an appropriate interest rate using a knowledge base.

---

## Features

* Automated outbound calling using Twilio Voice API
* Speech input capture in Hindi using Twilio Gather
* Multi-step conversational flow with branching and retries
* Dynamic text-to-speech audio generation using gTTS
* Session state management using CallSid
* Loan rate lookup using a JSON knowledge base
* Structured logging of call metadata for analytics
* Fully backend-driven solution; no frontend required
* Local development supported using ngrok

---

## Tech Stack

* Python 3.9+
* Flask
* Twilio Programmable Voice API
* Twilio Speech Recognition
* gTTS (Google Text-to-Speech)
* Pandas and openpyxl
* Ngrok
* JSON-based configuration

---

## Repository Structure

```
├── app.py                     # Main Flask server and IVR logic
├── make_call.py               # Script to initiate outbound calls
├── generate_summary.py        # Dynamic TTS audio generation
├── create_static_phrases.py   # Generates reusable audio prompts
├── utils.py                   # Logging and helper functionality
├── kb.json                    # Interest rate lookup table
├── requirements.txt           # Python dependencies
├── responses/                 # Generated audio response files
└── call_logs.xlsx             # Logged call metadata (created at runtime)
```

---

## Installation and Setup

### 1. Clone the Repository

```
git clone https://github.com/your-username/twilio-loan-voice-bot.git
cd twilio-loan-voice-bot
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxx
TWILIO_PHONE_NUMBER=+1XXXXXXXXXX
USER_PHONE_NUMBER=+91XXXXXXXXXX
```

Ensure `.env` is included in `.gitignore`.

### 4. Start the Flask Server

```
python app.py
```

### 5. Start ngrok to Expose Localhost

```
ngrok http 5000
```

Copy the generated HTTPS forwarding URL and update `make_call.py`:

```
url="https://your-ngrok-url.ngrok-free.app/voice"
```

### 6. Initiate a Call

```
python make_call.py
```

Your phone will receive a call, and the automated IVR will begin.

---

## Conversation Flow Overview

1. Introduction and user consent
2. Collect user name
3. Collect requested loan amount
4. Validate loan limit
5. Collect repayment tenure
6. Collect employment status
7. Determine interest rate from `kb.json`
8. Generate personalized spoken loan summary
9. Log captured call metadata
10. End call

---

## Call Logging

All completed calls are logged to `call_logs.xlsx`, including:

* Twilio CallSid
* Caller phone number
* Extracted name
* Loan amount
* Requested tenure
* Computed interest rate
* Employment status
* Confirmation status

This enables post-call analysis, follow-up, and CRM integration.

---

## Knowledge Base (Loan Rate Mapping)

Defined in `kb.json`:

```
{
  "12": 10.5,
  "24": 11.0,
  "36": 11.5
}
```

Extendable to support additional business rules.

---

## Potential Applications

* Automated loan outreach and qualification
* Fintech onboarding workflows
* Call center workload reduction
* Regional language engagement systems
* Pre-screening before human agent routing

---

## Future Enhancements

* Database logging (PostgreSQL or Supabase)
* Deployment to cloud hosting platforms
* Support for multiple languages
* Real-time CRM integration
* Web dashboard for call analytics

---

## Security Considerations

* Do not commit Twilio credentials or `.env` files
* Use secure authentication for deployments
* Do not process real user data without consent
* Follow applicable telecom and lending regulations

---

## Contributing

Contributions, suggestions, and issue reports are welcome. Please open a pull request or discussion thread.

---

## Contact

Tanush Mehta

Email: [tanushmehta05@gmail.com](mailto:tanushmehta05@gmail.com)

LinkedIn: [https://linkedin.com/in/tanush-mehta-9a55b5280](https://linkedin.com/in/tanush-mehta-9a55b5280)

```}
```
