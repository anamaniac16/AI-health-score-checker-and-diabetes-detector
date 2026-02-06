import requests
import os




def send_sms_alert(phone_number, patient_name, hospital_link):
    """
    Sends a real SMS alert using Fast2SMS API.
    Triggered ONLY during RED (critical) risk condition.
    """

    # Fast2SMS API endpoint
    url = "https://www.fast2sms.com/dev/bulkV2"

    # SMS message content
    message = (
        "🚨 EMERGENCY HEALTH ALERT 🚨\n"
        f"Patient: {patient_name}\n"
        "Critical health condition detected.\n"
        "Immediate medical attention required.\n"
        f"Hospital Location: {hospital_link}"
    )

    # Request payload
    payload = {
        "route": "v3",
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "numbers": phone_number
    }

    # Headers with API key from environment variable
    headers = {
        "authorization": os.getenv("FAST2SMS_API_KEY"),
        "Content-Type": "application/json"
    }

    # API request
    try:
        response = requests.post(url, json=payload, headers=headers)

        # Return API response for logging/debugging
        return response.json()

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
