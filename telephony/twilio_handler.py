from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# -------------------------------
# 1️⃣ INCOMING CALL HANDLER
# -------------------------------
@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()

    # Speak like a human
    response.say(
        "Hello. Welcome to the bank voice assistant. "
        "You can ask about account balance, loans, cards, or U P I issues.",
        voice="alice",
        language="en-IN"
    )

    # Listen to customer speech
    gather = Gather(
        input="speech",
        action="/process_speech",
        method="POST",
        timeout=5,
        speechTimeout="auto",
        language="en-IN"
    )

    gather.say(
        "Please tell me how I can help you.",
        voice="alice",
        language="en-IN"
    )

    response.append(gather)

    # If no speech
    response.say(
        "Sorry, I did not hear anything. Please call again.",
        voice="alice",
        language="en-IN"
    )

    return str(response)


# -------------------------------
# 2️⃣ PROCESS CUSTOMER SPEECH
# -------------------------------
@app.route("/process_speech", methods=["POST"])
def process_speech():
    response = VoiceResponse()

    user_speech = request.form.get("SpeechResult", "")

    print("Customer said:", user_speech)

    # Temporary reply (later replaced by AI)
    response.say(
        f"You said: {user_speech}. "
        "This will be processed by the banking AI system.",
        voice="alice",
        language="en-IN"
    )

    response.say(
        "Thank you for calling. Goodbye.",
        voice="alice",
        language="en-IN"
    )

    response.hangup()

    return str(response)


# -------------------------------
# 3️⃣ START SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
