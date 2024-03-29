import os
import yaml

CONFIG_FILE = os.environ.get("CONFIG_FILE")
if CONFIG_FILE is None:
    CONFIG_FILE = '/run/secrets/config'


class ConfigParser:
    def __init__(self, config):
        content = None
        with open(config, 'r') as fd:
            try:
                content = yaml.safe_load(fd)
            except yaml.YAMLError as e:
                print(e)

        self.Version = content['version']

        self.DB_Host = content['influxdb']['host']
        self.DB_Organization = content['influxdb']['organization']
        self.DB_Token = content['influxdb']['token']
        self.DB_DiagnosisBucket = content['influxdb']['bucket']['diagnosis']
        self.DB_HealthCheckBucket = content['influxdb']['bucket']['healthcheck']

        self.Slack_WebhookURL = content['slack']['webhookurl']
        self.Slack_Channel = content['slack']['channel']

        self.WatchInterval = content['watch']['interval']
        self.WatchPeriod = content['watch']['period']
        self.Threshold = content['watch']['threshold']

        self.Visualization_URL = content['slack']['urls']['visualization']
        self.InfluxDB_URL = content['slack']['urls']['influxdb']


config = CONFIG_FILE
__debug_config = '../config.yml'
if os.path.isfile(__debug_config):
    config = __debug_config
Config = ConfigParser(config)
