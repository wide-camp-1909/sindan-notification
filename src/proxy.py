from config import Config
from consts import CampaignKey, DiagnosisKey, ResultType
import influxdb2
from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
import json


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
        if jbody[DiagnosisKey.RESULT] == ResultType.INFO:
            return
        sendkeys = [
            DiagnosisKey.GROUP, DiagnosisKey.TYPE, DiagnosisKey.UUID,
            DiagnosisKey.RESULT, DiagnosisKey.TARGET, DiagnosisKey.OCCURR
        ]
        self.influxdb_cli.write_diagnosis_logs(jbody[DiagnosisKey.LAYER], [(k, jbody[k]) for k in sendkeys])
        return

    def __campaign(self, jbody):
        return


class ProxyServer:
    def __init__(self, ip='0.0.0.0', port=8000):
        print("Proxy started.")
        ThreadingHTTPServer((ip, port), RequestHandler).serve_forever()


if __name__ == '__main__':
    ProxyServer()
