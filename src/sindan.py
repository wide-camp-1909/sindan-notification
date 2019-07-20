import influxdb2
import time


class HealthStatus:
    GREEN = 'GREEN'
    RED = 'RED'


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
        statuslst = []
        for layer in ('datalink', 'interface', 'localnet', 'globalnet', 'dns', 'web'):
            health_record = self.influxdb_cli.read_health_status(layer, time_range, limit=1)
            last_st = health_record[0]['status']
            result_failed = self.influxdb_cli.read_diagnosis_logs(layer, time_range, ['result'], ['fail'])
            current_st = None

            # 通知はメッセージをまとめたいのでバッチ処理する
            if len(result_failed) < self.threshold:
                current_st = HealthStatus.GREEN
                if last_st == HealthStatus.RED:
                    self.__recover_notification()
            else:
                # キャンペーンUUIDと計測タイプのリストを取得，まとめてSlackに投稿
                current_st = HealthStatus.RED
                if last_st == HealthStatus.GREEN:
                    self.__down_notification()
            statuslst.append((layer, current_st))
        self.influxdb_cli.write_health_status(statuslst)

    def __recover_notification(self):
        pass

    def __down_notification(self):
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
