import json
import requests


def slack(channel, text, username='notifier', icon_emoji=':rocket:'):
    SLACK_URL = 'https://fool.slack.com/services/hooks/incoming-webhook?token=OYN4FwbP08GJuj9SSqIqjMZB'

    payload = json.dumps({
        'channel': channel,
        'username': username,
        'text': text,
        'icon_emoji': icon_emoji
    })

    response = requests.post(SLACK_URL, data=payload)
    return response.ok
