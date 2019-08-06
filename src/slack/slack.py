from config import Config
from consts import *
import datetime
import json
import os
import requests
import time


class Client:
    def __init__(self, webhook_url, channel, visualization_url, influxdb_url, debug=False):
        self.webhook_url = webhook_url
        self.channel = channel
        self.visualization_url = visualization_url
        self.influxdb_url = influxdb_url
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

    def send_failure_message(self, failures):
        text = '{n}件の新しいアラートが上がりました :bomb:'.format(n=len(failures))

        attachments = [{
                'title': '{layer}の障害'.format(layer=DESCRIPTION[layer].Short),
                'text': '{layer}では以下の正常性を確認します\n'.format(layer=DESCRIPTION[layer].Short) +
                        '\n'.join(map(lambda x: '\t• ' + x, DESCRIPTION[layer].Long)),
                'fallback': '{layer}の障害'.format(layer=DESCRIPTION[layer].Short),
                'color': 'danger',
                'fields': [{
                    'title': alert['type'],
                    'value': '*発生日時:* {ts}\n*UUID:* {uuid}'.format(ts=alert['ts'], uuid=alert['uuid']),
                    'short': True
                } for alert in alertlst],
                'footer': 'SINDAN Notifier {version}'.format(version=Config.Version),
                'ts': '{timestamp}'.format(timestamp=int(time.time())),
        } for layer, alertlst in failures]

        attachments.append({
            'pretext': '詳細はログデータベースを参照してください',
            'color': '#BBBBBB',
            'actions': [
                {'type': 'button', 'text': 'SINDAN Web を開く', 'url': self.visualization_url, 'style': 'primary'},
                {'type': 'button', 'text': 'InfluxDB Dashboard を開く', 'url': self.influxdb_url, 'style': 'primary'},
            ],
        })

        return self.__post(attachments, text=text)

    def send_recover_message(self, events):
        pass


if __name__ == '__main__':
    # Must to re-generate WebHook URL after debugging
    webhook_url = 'https://hooks.slack.com/services/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'
    cli = Client(webhook_url, 'sindan-dev')

    e1 = [LayerType.LOCALNET, [{'ts': '8/5 11:25:32', 'uuid': 'qwerty', 'type': LogType.V4.PING_GW}]]
    e2 = [LayerType.GLOBALNET, [{'ts': '8/5 11:25:32', 'uuid': 'qwerty', 'type': LogType.V4.PING_WWW}]]
    e3 = [LayerType.DNS, [
        {'ts': '8/5 11:25:32', 'uuid': 'qwerty', 'type': LogType.V4.DNS.DU_AAAA},
        {'ts': '8/5 11:25:32', 'uuid': 'qwerty', 'type': LogType.V4.DNS.V6_AAAA}
    ]]
    f = [e1, e2, e3]

    res = cli.send_failure_message(f)
    print(res)