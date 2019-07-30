import yaml


class ConfigParser:
    def __init__(self, config='./config.yml'):
        content = None
        with open(config, 'r') as fd:
            try:
                content = yaml.safe_load(fd)
            except yaml.YAMLError as e:
                print(e)

        # self.Proxy_IP = content['proxy']['ip']
        # self.Proxy_Port = content['proxy']['port']
        self.Proxy_IP = '0.0.0.0'
        self.Proxy_Port = '8000'

        self.DB_Host = content['influxdb']['host']
        self.DB_Organization = content['influxdb']['organization']
        self.DB_Token = content['influxdb']['token']
        self.DB_DiagnosisBucket = content['influxdb']['diagnosis_bucket']
        self.DB_HealthCheckBucket = content['influxdb']['healthcheck_bucket']


Config = ConfigParser()
