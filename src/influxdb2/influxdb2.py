import time
import requests


class HealthStatus:
    GREEN = 0
    RED = 1


class InfluxDB2:
    def __init__(self, db=None, token=None, organization=None, bucket_diagnosis=None, bucket_health=None):
        self.db = db
        self.token = token
        self.organization = organization
        self.bucket_diagnosis = bucket_diagnosis
        self.bucket_health = bucket_health

    def __write(self, bucket, data):
        endpoint = 'http://{db}:9999/api/v2/write'.format(db=self.db)
        headers = {
            'Authorization': 'Token {token}'.format(token=self.token)
        }
        params = (
            ('org', self.organization),
            ('bucket', bucket),
            ('precision', 'ms')
        )
        data_with_ts = data + ' {timestamp}'.format(timestamp=int(time.time()*1000))

        retry = 3
        while retry > 0:
            try:
                response = requests.post(endpoint, headers=headers, params=params, data=data_with_ts)
            except requests.exceptions.Timeout:
                retry -= 1
                continue
            else:
                return 0, response
        return 1, None

    def __read(self, data):
        pass

    def write_health_status(self):
        pass

    def read_health_status(self):
        pass

    def read_diagnosis_logs(self, time_range='-5minute'):
        pass


if __name__ == '__main__':
    db = 'localhost'
    token = 'eJdouF5UC7fuMuBn3Xce_tVB8LU0pwsrRBbMdGpzxEeOsVHo_YjiB7Y3k2FG0fUUMzyNFn9TDiaFppxW-rkYdw=='
    org = 'lab'
    bucket = 'sindan'
    data = 'mem,host=host1 used_percent=50.0'

    client = InfluxDB2(db=db, token=token, organization=org)
