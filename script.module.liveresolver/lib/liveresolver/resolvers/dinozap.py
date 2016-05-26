# -*- coding: utf-8 -*-


import re,urllib,urlparse,json,base64
from liveresolver.modules import client,decryptionUtils
from liveresolver.modules.log_utils import log
def resolve(url):
    #try:
        pageUrl = url
        try: referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except: referer = url
        
        result = client.request(url, referer=referer, headers= { 'Host': urlparse.urlparse(url).netloc} )
        page2 = re.findall('.*src=["\']([^"\']+)["\'].*',result)[0]
        result = client.request(page2, referer=referer )
        result = decryptionUtils.doDemystify(result)
        log(result)
        vs = re.findall('type="hidden" id=".+?" value="(.+?)"',result)
        for v in vs:
            vd = base64.b64decode(v)
            if 'm3u8' in vd:
                file = vd
        host = urlparse.urlparse(pageUrl).netloc
        origin = 'http://' + host
        url = file + '|%s' % urllib.urlencode({'Referer':pageUrl,'User-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0','Accept-Encoding':'gzip,deflate lzma, sdch','DNT':'1','Connection':'keep-alive','Icy-Metadata':'0','Origin':origin,'Host':host})
        return url
    #except:
    #    return
