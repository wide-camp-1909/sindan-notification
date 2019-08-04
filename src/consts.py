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


ShortDesc = lambda key: DESCRIPTION[key][0]
LongDesc = lambda key: DESCRIPTION[key][1]


DESCRIPTION = {
    LayerType.DATALINK:     ('データリンク層', ('リンク状態の確認')),
    LayerType.INTERFACE:    ('インターフェイス層', ()),
    LayerType.LOCALNET:     ('ローカルネットワーク層', ()),
    LayerType.GLOBALNET:    ('グローバルネットワーク層', ()),
    LayerType.DNS:          ('名前解決層', ()),
    LayerType.WEB:          ('ウェブアプリケーション層', ()),
    LogType.IFSTATUS:       '',
    LogType.V4.AUTOCONF:    '',
    LogType.V4.PING_DNS:    '',
    LogType.V4.PING_GW:     '',
    LogType.V4.PING_WWW:    '',
    LogType.V4.DNS.DU_A:    '',
    LogType.V4.DNS.DU_AAAA: '',
    LogType.V4.DNS.V4_A:    '',
    LogType.V4.DNS.V4_AAAA: '',
    LogType.V4.DNS.V6_A:    '',
    LogType.V4.DNS.V6_AAAA: '',
    LogType.V4.HTTP:        '',
    LogType.V6.AUTOCONF:    '',
    LogType.V6.PING_DNS:    '',
    LogType.V6.PING_GW:     '',
    LogType.V6.PING_WWW:    '',
    LogType.V6.DNS.DU_A:    '',
    LogType.V6.DNS.DU_AAAA: '',
    LogType.V6.DNS.V4_A:    '',
    LogType.V6.DNS.V4_AAAA: '',
    LogType.V6.DNS.V6_A:    '',
    LogType.V6.DNS.V6_AAAA: '',
    LogType.V6.HTTP:        ''
}
