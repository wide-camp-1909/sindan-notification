import influxdb2
import time


class HealthStatus:
    GREEN = 1
    RED = 0


class Watch:
    def __init__(self, watch_params=None, db_params=None, slack_params=None, debug=False):
        self.watch_period = watch_params['period']
        self.watch_interval = watch_params['interval']
        self.threshold = watch_params['threshold']
        self.influxdb_cli = influxdb2.Client(
            db=db_params['db'], token=db_params['token'], organization=db_params['organization'],
            bucket_diagnosis=db_params['bucket_diagnosis'], bucket_health=db_params['bucket_health'], debug=debug)
        self.slack_cli = None
        self.debug = debug

    def __update_health_status(self):
        now_ts = round(time.time() * 1000)
        time_range = '-{period}'.format(period=self.watch_period)
        for layer in ('datalink', 'interface', 'localnet', 'globalnet', 'dns', 'web'):
            pass

    def run(self):
        """ MEMO
        方針: 機関においてしきい値以上の 'fail' レコードが存在する場合は HealthStatus を RED にする
        1. 期間における 'fail' のレコードを全件取得し個数を数える
        2. しきい値を超えている場合は HealthStatus を RED とし現在のタイムスタンプでレコードを追加
          2-1. 超えていなければ HealthStatus を GREEN とし現在のタイムスタンプでレコードを追加
        3. HealthStatus が変化するタイミングをトリガ
          3-1. 通知送信
        """
        pass
