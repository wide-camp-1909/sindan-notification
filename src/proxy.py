import influxdb2
from bottle import route, run
from bottle import post, get, request, response
import json


if __name__ == '__main__':
    ProxyServer(host='127.0.0.1', port=8081, debug=True)
