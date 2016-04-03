# -*- coding: utf-8 -*-


import re,urlparse
from liveresolver.modules import client
from liveresolver.modules.log_utils import log
def resolve(url):
    #try:
        
        
        result = client.request(url)
        log(result)
        urls = re.findall('<i?frame.+?src=(?:\'|\")(.+?)(?:\'|\")',result)
        for url in urls:
            if 'player' in url and 'advert' not in url:
                rr = url
                break
        result = client.request(rr)   
        log(result)
        pom = re.findall('.*?url:\s[\'"](\/\/streamaccess\.unas\.tv[^\'"]+\" \+ label \+ \"[^\'"]+).*?', result)[0].replace('" + label + "','laola1tv')
        result = client.request('http:' +pom, referer='http://www.laola1.tv/swf/videoplayer.swf?r=20150305', mobile=True)
        auth,url = re.findall('.*?auth="([^\'"]+)"\s*url="([^\'"]+)".*?',result)[0]
        url = url + '?hdnea='+ auth 
        return url
    #except:
    #    return

