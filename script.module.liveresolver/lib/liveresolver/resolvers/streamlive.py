# -*- coding: utf-8 -*-


import re,urlparse,json,requests,cookielib
from liveresolver.modules import client
from liveresolver.modules import control
from liveresolver.modules import constants
from liveresolver.modules.log_utils import log
import urllib,sys,os

cookieFile = os.path.join(control.dataPath, 'streamlivecookie.lwp')


def resolve(url):
    
    try:
        page = url
        addonid = 'script.module.liveresolver'

        user, password = control.setting('streamlive_user'), control.setting('streamlive_pass')
        if (user == '' or password == ''):
            user, password = control.addon(addonid).getSetting('streamlive_user'), control.addon(addonid).getSetting('streamlive_pass')
        if (user == '' or password == ''): return ''

        try: 
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
            url = url.replace(referer,'').replace('?referer=','').replace('&referer=','')
        except:
            referer = url


        session = start_session()
        post_data = 'username=%s&password=%s&accessed_by=web&submit=Login'%(user,password)

        session.cookies = cookielib.LWPCookieJar(cookieFile)
        if not os.path.exists(cookieFile):
            #make new cookie file, and request new login cookies
            session.cookies.save()
            session = login(session,post_data)
        else:
            pass

        result = session.get(url).text


        if 'this channel is a premium channel.' in result.lower():
          control.infoDialog('Premium channel. Upgrade your account to watch it!', heading='Streamlive.to')
          return 

        if 'not logged in yet' in result.lower():
            #Cookie expired or not valid, request new cookie
            session = login(session,post_data) 
            result = session.get(url).text

        if 'captcha' in result:
            try:
                answer = re.findall('Question\:.+?\:(.+?)<',result)[0].strip()
            except:
                answer = eval(re.findall('Question\:(.+?)<',result)[0].replace('=?',''))
            
            post = urllib.urlencode({"captcha":answer})
            result = session.post(page, data=post, headers={'referer':referer, 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to'}).text
        
        token_url = re.compile('getJSON\("(.+?)"').findall(result)[0]
        r2 = client.request(token_url,referer=referer)
        token = json.loads(r2)["token"]

        file = re.compile('file\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace('.flv','')
        rtmp = re.compile('streamer\s*:\s*(?:\'|\")(.+?)(?:\'|\")').findall(result)[0].replace(r'\\','\\').replace(r'\/','/')
        app = re.compile('.*.*rtmp://[\.\w:]*/([^\s]+)').findall(rtmp)[0]
        url=rtmp + ' app=' + app + ' playpath=' + file + ' swfUrl=http://www.streamlive.to/ads/streamlive.swf flashver=' + constants.flash_ver() + ' live=1 timeout=15 token=' + token + ' swfVfy=1 pageUrl='+page

        
        return url
    except:
        return


def start_session():
    s = requests.Session()
    html = s.get('http://www.streamlive.to', headers={'referer':'http://www.streamlive.to', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()}).text
    if 'captcha' in html:
        try:
            answer = re.findall('Question\:.+?\:(.+?)<',html)[0].strip()
        except:
            answer = eval(re.findall('Question\:(.+?)<',html)[0].replace('=?',''))
        
        post = urllib.urlencode({"captcha":answer})
        html = s.post('http://www.streamlive.to', data=post, headers={'referer': 'http://www.streamlive.to', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()}).text
        
    return s

def login(session,post_data):
    log('Making new login token.')
    session.cookies.load(ignore_discard=True)
    session.post('http://www.streamlive.to/login.php', data=post_data, headers = {'referer':'http://www.streamlive.to/login', 'Content-type':'application/x-www-form-urlencoded', 'Origin': 'http://www.streamlive.to', 'Host':'www.streamlive.to', 'User-agent':client.agent()})
    session.cookies.save(ignore_discard=True)
    return  session