import datetime
import json
import os
import requests
import time


class Client:
    def __init__(self, webhook_url, channel, debug=False):
        self.webhook_url = webhook_url
        self.channel = channel
        self.debug = debug

    def __post(self, attachments, text=None, max_retry=3):
        payload = {
            'channel': self.channel,
            'attachments': json.dumps(attachments)
        }

        if text is not None:
            payload['text'] = text

        while max_retry > 0:
            try:
                response = requests.post(self.webhook_url, data=payload)
            except requests.exceptions.Timeout:
                max_retry -= 1
                continue
            else:
                return True, response
        return False, None

    def send_failure_message(self, alertlst):
        pass


if __name__ == '__main__':
    # Must to re-generate WebHook URL after debugging
    webhook_url = 'https://hooks.slack.com/services/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'
    cli = Client(webhook_url=webhook_url, broadcast_channel='sindan')
    cli.send_failure_message(None)