from config import Config
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
            'attachments': attachments
        }

        if text is not None:
            payload['text'] = text

        while max_retry > 0:
            try:
                response = requests.post(self.webhook_url, data=json.dumps(payload))
            except requests.exceptions.Timeout:
                max_retry -= 1
                continue
            else:
                return True, response
        return False, None

    def send_failure_message(self, alertlst):
        attachments = [
            {
                'title': 'Room301_5Gでローカルネットワーク層の障害 :bomb:',
                'text': 'ローカルネットワーク層では以下の正常性を確認します\n'
                        '\t• デフォルトGWへのICMP到達性\n',
                'fallback': 'Room301_5Gでローカルネットワーク層の障害が発生しました',
                'color': 'danger',
                'fields': [
                    {
                        'title': 'V4.PING_GW',
                        'value': '2019/07/21 22:06:26\n'
                                 '`40d995c2`',
                        'short': True
                    },
                ],
                'footer': 'SINDAN Notifier v1.1.0',
                'ts': '{}'.format(int(time.time())),
            },
            {
                'title': 'Room301_5Gで名前解決層の障害 :bomb:',
                'text': '名前解決層では以下の正常性を確認します\n'
                        '\t• IPv4による名前解決\n'
                        '\t• IPv6による名前解決',
                'fallback': 'Room301_5Gで名前解決層の障害が発生しました',
                'color': 'danger',
                'fields': [
                    {
                        'title': 'V4.DNS.V4_AAAA',
                        'value': '2019/07/21 22:06:26\n'
                                 '`40d995c2`',
                        'short': True
                    },
                    {
                        'title': 'V4.DNS.V6_AAAA',
                        'value': '2019/07/21 22:06:26\n'
                                 '`40d995c2`',
                        'short': True
                    },
                    {
                        'title': 'V4.DNS.DUAL_AAAA',
                        'value': '2019/07/21 22:06:26\n'
                                 '`40d995c2`',
                        'short': True
                    },
                ],
                'footer': 'SINDAN Notifier v1.1.0',
                'ts': '{}'.format(int(time.time())),
            },
            {
                'title': 'Room301_5Gでウェブアプリケーション層の障害 :bomb:',
                'text': 'ウェブアプリケーション層では以下の正常性を確認します\n'
                        '\t• HTTP通信\n',
                'fallback': 'Room301_5Gでウェブアプリケーション層の障害が発生しました',
                'color': 'danger',
                'fields': [
                    {
                        'title': 'V4.HTTP',
                        'value': '2019/07/21 22:06:26\n'
                                 '`40d995c2`',
                        'short': True
                    },
                    {
                        'title': 'V6.HTTP',
                        'value': '2019/07/21 22:06:26\n'
                                 '`40d995c2`',
                        'short': True
                    },
                ],
                'footer': 'SINDAN Notifier v1.1.0',
                'ts': '{}'.format(int(time.time())),
            },
            {
                'pretext': '詳細はログデータベースを参照してください',
                'color': '#000000',
                'actions': [
                    {
                        'type': 'button',
                        'text': 'SINDAN Web を開く',
                        'url': 'http://example.com/',
                        'style': 'primary'
                    },
                    {
                        'type': 'button',
                        'text': 'InfluxDB Dashboard を開く',
                        'url': 'http://example.com/',
                        'style': 'primary'
                    },
                ],
            },
        ]

        return self.__post(attachments, text='3件の新しいアラートが上がりました')


if __name__ == '__main__':
    # Must to re-generate WebHook URL after debugging
    webhook_url = 'https://hooks.slack.com/services/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'
    cli = Client(webhook_url, 'sindan')
    res = cli.send_failure_message(None)
    print(res)