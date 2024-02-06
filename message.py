import network
import urequests
import json
import ubinascii

def send_email(to_email, subject, text):
    mailgun_domain = 'sandboxd7542b626afc4af083f24901bc5f8487.mailgun.org'
    mailgun_api_key = 'de04442b5c7bb80a4013564a2a9b84a7-1c7e8847-6e8b2801'
    url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"

    headers = {
        'Authorization': 'Basic ' + ubinascii.b2a_base64(b'api:' + bytes(mailgun_api_key, 'utf-8')).decode().strip(),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # URL-encode the form data
    data = 'from={}&to={}&subject={}&text={}'.format(
        'Object Security <Security@{}>'.format(mailgun_domain),
        to_email,
        subject,
        text
    )

    response = urequests.post(url, data=data, headers=headers)
    print(response.text)
    response.close()


def connect_to_wifi():
    SSID = 'NUdormitory'
    PASSWORD = '1234512345'
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    i = 0
    while not wlan.isconnected():
        pass
    print("Connected to WiFi")