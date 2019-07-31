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

        self.DB_Host = content['influxdb']['host']
        self.DB_Organization = content['influxdb']['organization']
        self.DB_Token = content['influxdb']['token']
        self.DB_DiagnosisBucket = content['influxdb']['bucket']['diagnosis']
        self.DB_HealthCheckBucket = content['influxdb']['bucket']['healthcheck']


# Config = ConfigParser('./config.yml')
Config = ConfigParser(CONFIG_FILE)
