from consts import *
import influxdb2
import slack
import time


class HealthStatus:
    GREEN = 'GREEN'
    RED = 'RED'


class AlertTrigger:
    FAILURE = 'failure'
    RECOVER = 'recover'


class Watch:
    def __init__(self, watch_params=None, db_params=None, slack_params=None, debug=False):
        self.watch_period = watch_params['period']
        self.watch_interval = watch_params['interval']
        self.threshold = watch_params['threshold']
        self.influxdb_cli = influxdb2.Client(db_params['db'], db_params['token'], db_params['organization'],
                                             db_params['bucket_diagnosis'], db_params['bucket_health'], debug=debug)
        self.slack_cli = slack.Client(slack_params['webhook_url'], slack_params['channel'], debug=False)
        self.debug = debug

    def __update_health_status(self):
        rt = []
        statuslst = []
        time_range = '-{period}'.format(period=self.watch_period)
        for layer in LayerType.TypeList:
            last_st = self.influxdb_cli.read_health_status(layer, time_range, limit=1)[0]['status']
            result_failed = self.influxdb_cli.read_diagnosis_logs(layer, time_range,
                                                                  [DiagnosisKey.RESULT], [ResultType.FAIL])
            if len(result_failed) < self.threshold:
                current_st = HealthStatus.GREEN
                if last_st == HealthStatus.RED:
                    rt.append({
                        'layer': layer,
                        'trigger': AlertTrigger.RECOVER
                    })
            else:
                current_st = HealthStatus.RED
                if last_st == HealthStatus.GREEN:
                    rt.append({
                        'layer': layer,
                        'trigger': AlertTrigger.FAILURE,
                        'ts': [r['_time'] for r in result_failed]
                    })
            statuslst.append((layer, current_st))
        self.influxdb_cli.write_health_status(statuslst)
        return rt

    def __notification_on_failure(self, eventlst):
        if not eventlst:
            return
        alertlst = []
        for event in eventlst:
            layer = event['layer']
            alert = []
            for ts in event['ts']:
                uuid = self.influxdb_cli.read_diagnosis_logs(layer, fieldlst=[DiagnosisKey.UUID], ts=ts)
                dtype = self.influxdb_cli.read_diagnosis_logs(layer, fieldlst=[DiagnosisKey.TYPE], ts=ts)
                desc = DESCRIPTION[dtype]
                alert.append({
                    'ts': ts,
                    'uuid': uuid,
                    'type': dtype,
                    'desc': desc
                })
            alertlst.append([layer, alert])
        # call slack method here

    def __notification_on_recover(self, eventlst):
        if not eventlst:
            return
        # call slack method here

    def run(self):
        while True:
            rt = self.__update_health_status()
            if not rt:
                continue
            self.__notification_on_failure([event for event in rt if event['trigger'] == AlertTrigger.FAILURE])
            self.__notification_on_recover([event for event in rt if event['trigger'] == AlertTrigger.RECOVER])
            time.sleep(self.watch_interval)