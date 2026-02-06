from sms_service import send_sms_alert

resp = send_sms_alert(
    "YOUR_10_DIGIT_NUMBER",
    "Test Patient",
    "https://www.google.com/maps"
)

print(resp)
