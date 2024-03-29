import datetime
import requests
import time
import uuid


class Client:
    def __init__(self, db, token, organization, bucket_diagnosis, bucket_health, debug=False):
        self.db = db
        self.token = token
        self.organization = organization
        self.bucket_diagnosis = bucket_diagnosis
        self.bucket_health = bucket_health
        self.debug = debug

    @staticmethod
    def __post_requests(endpoint, **kwargs):
        retry = 3
        while retry > 0:
            try:
                response = requests.post(endpoint, **kwargs)
            except requests.exceptions.Timeout:
                retry -= 1
                continue
            else:
                return True, response
        return False, None

    @staticmethod
    def __build_ifql(bucket, time_range, filterlst=None, reverse=False, limit=None):
        ifql = [
            'from(bucket: "{bucket}")'.format(bucket=bucket),
            'range(start:{range})'.format(range=time_range)
        ]
        if filterlst is not None:
            for f in filterlst:
                ifql.append('filter(fn: (r) => r.{key} == "{value}")'.format(key=f[0], value=f[1]))
        if reverse is True:
            ifql.append('sort(columns: ["_time"], desc: true)')
        if limit is not None:
            ifql.append('limit(n:{limit})'.format(limit=limit))
        return ' |> '.join(ifql)

    @staticmethod
    def __parse_csv_response(content):
        csv = [row.split(',') for row in content.split('\r\n')]
        dictlst = []
        for row in csv[1:]:
            dic = {csv[0][i]: str(data) for i, data in enumerate(row) if csv[0][i] != ''}
            if len(dic) > 0:
                dictlst.append(dic)
        return dictlst

    def __write(self, bucket, measurement, kvs):
        endpoint = 'http://{db}:9999/api/v2/write'.format(db=self.db)
        headers = {
            'Authorization': 'Token {token}'.format(token=self.token)
        }
        params = [
            ('org', self.organization),
            ('bucket', bucket),
            ('precision', 'ms')
        ]
        flat_kvs = ','.join(map(lambda kv: '{key}="{value}"'.format(key=kv[0], value=kv[1]), kvs))
        timestamp = round(time.time() * 1000)
        line_protocol = '{measurement} {flat_kvs}  {timestamp}'\
            .format(measurement=measurement, flat_kvs=flat_kvs, timestamp=timestamp)
        if self.debug:
            print('InfluxDB2.Client.__write:', line_protocol)
        return self.__post_requests(endpoint, headers=headers, params=params, data=line_protocol)

    def __read(self, bucket, time_range='-1m', filterlst=None, reverse=None, limit=None):
        endpoint = 'http://{db}:9999/api/v2/query'.format(db=self.db)
        headers = {
            'Authorization': 'Token {token}'.format(token=self.token),
            'Accept': 'application/csv',
            'Content-Type': 'application/vnd.flux'
        }
        params = [
            ('org', self.organization)
        ]
        query = self.__build_ifql(bucket, time_range, filterlst=filterlst, reverse=reverse, limit=limit)
        if self.debug:
            print('InfluxDB2.Client.__read:', query)
        return self.__post_requests(endpoint, headers=headers, params=params, data=query)

    def write_health_status(self, statuslst):
        for layer, status in statuslst:
            ok, response = self.__write(self.bucket_health, layer, [('status', status)])
            if ok and self.debug:
                print('InfluxDB2.Client.write_health_status:', response)

    def read_health_status(self, layer, time_range='-5m', limit=None):
        filterlst = [('_measurement', layer), ('_field', 'status')]
        reverse_flag = False
        if limit is not None:
            reverse_flag = True
        ok, response = self.__read(self.bucket_health, time_range, filterlst, reverse_flag, limit)
        if ok and self.debug:
            print('InfluxDB2.Client.read_health_status:', response)
        return self.__parse_csv_response(response.content.decode('utf-8'))

    def write_diagnosis_logs(self, layer, details):
        ok, response = self.__write(self.bucket_diagnosis, layer, details)
        if ok and self.debug:
            print('InfluxDB2.Client.write_diagnosis_logs:', response)

    def read_diagnosis_logs(self, layer, time_range='-5m', fieldlst=None, valuelst=None, ts=None, limit=None):
        filterlst = [('_measurement', layer)]
        reverse_flag = False
        if fieldlst is not None:
            filterlst.extend([('_field', field) for field in fieldlst])
        if valuelst is not None:
            filterlst.extend([('_value', val) for val in valuelst])
        if limit is not None:
            reverse_flag = True
        ok, response = self.__read(self.bucket_diagnosis, time_range, filterlst, reverse_flag, limit)
        if ok and self.debug:
            print('InfluxDB2.Client.read_diagnosis_logs:', response)
        result = self.__parse_csv_response(response.content.decode('utf-8'))
        if ts is not None:
            for r in result:
                if r['_time'] == ts:
                    return r
        else:
            return result


class Tester:
    def __init__(self, client=None, **kwargs):
        self.client = client
        if self.client is None:
            self.client = Client(**kwargs)

    @staticmethod
    def __dummy_sindan_client():
        return (
            'dns',
            [
                ('log_group', 'IPv4'),
                ('log_type', 'v4dnsqry_A_ipv4.sindan-net.com'),
                ('log_campaign_uuid', str(uuid.uuid1())),
                ('result', 'success'),
                # ('target', ''),
                # ('detail', 'totemonagaidata'),
                ('occurred_at', datetime.datetime.now().strftime("%Y/%m/%d %T"))
            ]
        )

    def run(self, repeat=1):
        while repeat > 0:
            layer, details = self.__dummy_sindan_client()
            self.client.write_diagnosis_logs(layer, details)
            repeat -= 1


if __name__ == '__main__':
    db = 'localhost'
    # token = 'eJdouF5UC7fuMuBn3Xce_tVB8LU0pwsrRBbMdGpzxEeOsVHo_YjiB7Y3k2FG0fUUMzyNFn9TDiaFppxW-rkYdw=='
    token = 'NFcpZKbLaaAMB7GbbOzGrBBVZ17_dp4_CG5yj_iPWj2ZhrVwVLkBXZA0iBFSrI_qLC2B08xHT0OjhTAhiTd28A=='
    org = 'lab'
    bucket = 'sindan'

    client = Client(db, token, org, bucket_diagnosis=bucket, debug=True)
    Tester(client=client).run(repeat=3)
    # res = client.read_diagnosis_logs('dns', time_range='-1m')
    res = client.read_diagnosis_logs('dns', time_range='-10m', fieldlst=['result'], valuelst=['success'], limit=1)
    print(res)
