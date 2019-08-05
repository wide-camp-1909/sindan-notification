"""
Format Definitions
"""

"""
Campaign Logs
"""

class CampaignKey:
    UUID    = "log_campaign_uuid"
    MAC     = "mac_addr"
    OS      = "os"
    SSID    = "ssid"
    VERSION = "version"
    OCCURR  = 'occurred_at'


"""
Diagnosis Logs
"""

class DiagnosisKey:
    LAYER  = 'layer'
    GROUP  = 'log_group'
    TYPE   = 'log_type'
    UUID   = 'log_campaign_uuid'
    RESULT = 'result'
    TARGET = 'target'
    DETAIL = 'detail'
    OCCURR = 'occurred_at'


class LayerType:
    DATALINK  = 'datalink'
    INTERFACE = 'interface'
    LOCALNET  = 'localnet'
    GLOBALNET = 'globalnet'
    DNS       = 'dns'
    WEB       = 'web'
    TypeList  = [DATALINK, INTERFACE, LOCALNET, GLOBALNET, DNS, WEB]


class GroupType:
    COMMON = 'common'
    IPV4   = 'IPv4'
    IPV6   = 'IPv6'


class LogType:
    IFSTATUS = 'ifstatus'

    class V4:
        AUTOCONF = 'v4autoconf'
        PING_DNS = 'v4alive_namesrv'
        PING_GW  = 'v4alive_router'
        PING_WWW = 'v4alive_srv'

        class DNS:
            DU_A    = 'v4dnsqry_A_dual.sindan-net.com'
            DU_AAAA = 'v4dnsqry_AAAA_dual.sindan-net.com'
            V4_A    = 'v4dnsqry_A_ipv4.sindan-net.com'
            V4_AAAA = 'v4dnsqry_AAAA_ipv4.sindan-net.com'
            V6_A    = 'v4dnsqry_A_ipv6.sindan-net.com'
            V6_AAAA = 'v4dnsqry_AAAA_ipv6.sindan-net.com'

        HTTP = 'v4http_srv'

    class V6:
        AUTOCONF = 'v6autoconf'
        PING_DNS = 'v6alive_namesrv'
        PING_GW  = 'v6alive_router'
        PING_WWW = 'v6alive_srv'

        class DNS:
            DU_A    = 'v6dnsqry_A_dual.sindan-net.com'
            DU_AAAA = 'v6dnsqry_AAAA_dual.sindan-net.com'
            V4_A    = 'v6dnsqry_A_ipv4.sindan-net.com'
            V4_AAAA = 'v6dnsqry_AAAA_ipv4.sindan-net.com'
            V6_A    = 'v6dnsqry_A_ipv6.sindan-net.com'
            V6_AAAA = 'v6dnsqry_AAAA_ipv6.sindan-net.com'

        HTTP = 'v6http_srv'


class ResultType:
    FAIL    = '0'
    SUCCESS = '1'
    INFO    = '10'


"""
Description
"""


class D:
    def __init__(self, short_desc, long_desc):
        self.Short = short_desc
        self.Long = long_desc


DESCRIPTION = {
    LayerType.DATALINK:     D('データリンク層', ('L2の接続状態', 'Wi-FiのAssociation状態など')),
    LayerType.INTERFACE:    D('インターフェイス層', ('インターフェイスの自動アドレス設定', 'SLAAC, DHCP, DHCPv6')),
    LayerType.LOCALNET:     D('ローカルネットワーク層', ('内部ネットワークでの到達性', 'デフォルトGWへのICMP到達性など')),
    LayerType.GLOBALNET:    D('グローバルネットワーク層', ('外部ネットワークへの到達性', '外部サーバへのICMP到達性など')),
    LayerType.DNS:          D('名前解決層', ('IPv4の名前解決', 'IPv6の名前解決')),
    LayerType.WEB:          D('ウェブアプリケーション層', ('外部サーバへのHTTP通信')),
    LogType.IFSTATUS:       D('', ('')),
    LogType.V4.AUTOCONF:    D('', ('')),
    LogType.V4.PING_DNS:    D('', ('')),
    LogType.V4.PING_GW:     D('', ('')),
    LogType.V4.PING_WWW:    D('', ('')),
    LogType.V4.DNS.DU_A:    D('', ('')),
    LogType.V4.DNS.DU_AAAA: D('', ('')),
    LogType.V4.DNS.V4_A:    D('', ('')),
    LogType.V4.DNS.V4_AAAA: D('', ('')),
    LogType.V4.DNS.V6_A:    D('', ('')),
    LogType.V4.DNS.V6_AAAA: D('', ('')),
    LogType.V4.HTTP:        D('', ('')),
    LogType.V6.AUTOCONF:    D('', ('')),
    LogType.V6.PING_DNS:    D('', ('')),
    LogType.V6.PING_GW:     D('', ('')),
    LogType.V6.PING_WWW:    D('', ('')),
    LogType.V6.DNS.DU_A:    D('', ('')),
    LogType.V6.DNS.DU_AAAA: D('', ('')),
    LogType.V6.DNS.V4_A:    D('', ('')),
    LogType.V6.DNS.V4_AAAA: D('', ('')),
    LogType.V6.DNS.V6_A:    D('', ('')),
    LogType.V6.DNS.V6_AAAA: D('', ('')),
    LogType.V6.HTTP:        D('', ('')),
}
