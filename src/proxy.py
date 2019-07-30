import influxdb2
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import yaml
import json


class ProxyConfig:
    def __init__(self, config='./config.yml'):
        content = None
        with open(config, 'r') as fd:
            try:
                content = yaml.safe_load(fd)
            except yaml.YAMLError as e:
                print(e)
        self.Proxy_IP = content['proxy']['ip']
        self.Proxy_Port = content['proxy']['port']
        self.DB_Host = content['influxdb']['host']
        self.DB_Organization = content['influxdb']['organization']
        self.DB_Token = content['influxdb']['token']
        self.DB_DiagnosisBucket = content['influxdb']['diagnosis_bucket']
        self.DB_HealthCheckBucket = content['influxdb']['healthcheck_bucket']


Config = ProxyConfig()


class ProxyEndpoint:
    DiagnosisLog = '/sindan.log'
    CampaignLog = '/sindan.log_campaign'


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    pass


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.influxdb_cli = influxdb2.Client(
            Config.DB_Host, Config.DB_Token, Config.DB_Organization,
            Config.DB_DiagnosisBucket, Config.DB_HealthCheckBucket
        )
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.wfile.write(b'It works!')
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        return

    def do_POST(self):
        bytes = int(self.headers['Content-Length'])
        rawdata = self.rfile.read(bytes)
        jbody = json.loads(rawdata.decode('utf-8'))
        if self.path == ProxyEndpoint.DiagnosisLog:
            self.__diagnosis(jbody)
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            return
        if self.path == ProxyEndpoint.CampaignLog:
            self.__campaign(jbody)
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            return
        self.send_response(HTTPStatus.BAD_REQUEST)
        self.end_headers()
        return

    def __diagnosis(self, jbody):
        # process raw data
        print(self.influxdb_cli)
        print(jbody)  # debug
        pass

    def __campaign(self, jbody):
        # process raw data
        print(jbody)  # debug
        pass


class ProxyServer:
    def __init__(self, ip='0.0.0.0', port=8081):
        ThreadingHTTPServer((ip, port), RequestHandler).serve_forever()


if __name__ == '__main__':
    ProxyServer(ip=Config.Proxy_IP, port=Config.Proxy_Port)
