# -*- coding: utf-8 -*-


import re,urlparse,cookielib,os
from liveresolver.modules import client,recaptcha_v2,control,constants, decryptionUtils
from liveresolver.modules.log_utils import log
cookieFile = os.path.join(control.dataPath, 'finecastcookie.lwp')

def resolve(url):
    try:
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer=url


        id = urlparse.parse_qs(urlparse.urlparse(url).query)['u'][0]
        url = 'http://www.finecast.tv/embed4.php?u=%s&vw=640&vh=450'%id
        log(url)
        rs = client.request(url,referer=referer)
        sitekey = re.findall('data-sitekey="([^"]+)', rs)[0]
        token = recaptcha_v2.UnCaptchaReCaptcha().processCaptcha(sitekey, lang='en')
        token = {'g-recaptcha-response': token}


        result =client.request (url, post=urllib.urlencode(token),referer=referer)
        

        file = re.findall('[\'\"](.+?.stream)[\'\"]',result)[0]
        auth = re.findall('[\'\"](\?wmsAuthSign.+?)[\'\"]',result)[0]
        rtmp = 'http://play.finecast.tv:1935/live/%s/playlist.m3u8%s'%(file,auth)

        return rtmp

        
    except:
        return


def get_cj():
    cookieJar=None
    try:
        cookieJar = cookielib.LWPCookieJar()
        cookieJar.load(cookieFile,ignore_discard=True)
    except: 
        cookieJar=None

    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar