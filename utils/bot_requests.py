import requests


async def send_to_chat(bot_token, chat_id, message_text):
    # Create the request payload
    payload = {"chat_id": chat_id, "text": message_text, "parse_mode": "HTML"}

    # Send the request to send the inline keyboard message
    response = requests.post(
        f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload,
    )

    # Check the response status
    if response.status_code == 200:
        return response
    else:
        return False