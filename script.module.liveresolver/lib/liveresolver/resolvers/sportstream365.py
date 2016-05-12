# -*- coding: utf-8 -*-


import re,urlparse,json,time,socket
from liveresolver.modules import client,constants
from liveresolver.modules.log_utils import log

def resolve(url):
    try:
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url

        id = urlparse.parse_qs(urlparse.urlparse(url).query)['game'][0]

        ts = int(time.time())

        tk = 'http://sportstream365.com/LiveFeed/GetGame?lng=ru&id='+id+'&partner=24&_='+str(ts)

        html = client.request(tk,referer='http://www.sportstream365.com/')
        file = re.findall('.*?VI[\'"]*[:,]\s*[\'"]([^\'"]+)[\'"].*',html)[0]
        rt = _resolve('rtmpe://xlive.sportstream365.com/xlive')
        url = rt + ' playpath=raw:sl4_' + file + ' conn=S:client conn=S:3.1.0.9 conn=S:en live=1 timeout=15'
        return url
    except:
        return


def _resolve(src):
    parsed_link = urlparse.urlsplit(src)
    tmp_host = parsed_link.netloc.split(':')
    
    servers = ["93.189.58.42","185.28.190.158","178.175.132.210","178.17.168.90","185.56.137.178","94.242.254.72"]
    import random
    tmp_host[0] = random.choice(servers)
    
    tmp_host = ':'.join(tmp_host)
    parsed_link = parsed_link._replace(netloc=tmp_host)
    return parsed_link.geturl()