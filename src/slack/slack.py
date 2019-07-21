import datetime
import json
import os
import requests
import time


class Client:
    def __init__(self, token=None, broadcast_channel=None, debug=False):
        self.token = token
        self.broadcast_channel = broadcast_channel
        self.debug = debug

    def __post_attachments(self, attachments, text=None, to=None, at=None, ephemeral=False, max_retry=3):
        message_endpoint_url = 'https://slack.com/api/chat.postMessage'
        ephemeral_endpoint_url = 'https://slack.com/api/chat.postEphemeral'

        if to is None:
            to = self.broadcast_channel
        if at is None:
            at = self.broadcast_channel

        endpoint_url = message_endpoint_url
        payload = {
            'token': self.token,
            'channel': to,
            'attachments': json.dumps(attachments)
        }

        if text is not None:
            payload['text'] = text

        if ephemeral:
            endpoint_url = ephemeral_endpoint_url
            payload['user'] = to
            payload['channel'] = at

        retry = 0
        while True:
            try:
                res = requests.post(endpoint_url, data=payload)
                self.debug and print(res)
            except requests.exceptions.Timeout:
                retry += 1
                if retry == max_retry:
                    return 1, 'Connection Timeout'
                continue
            else:
                return 0, 'OK'
