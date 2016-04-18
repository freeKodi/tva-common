# -*- coding: utf-8 -*-


import re,urllib,urlparse,base64,json
from liveresolver.modules import client,constants,liveresolver_utils
from liveresolver.modules.log_utils import log
import requests
def resolve(url):
    #try:
        s = requests.Session()
        try:
            referer = urlparse.parse_qs(urlparse.urlparse(url).query)['referer'][0]
        except:
            referer= url 


        ref = liveresolver_utils.remove_referer(url)
        result = s.get(url, headers={'Referer':referer,'User-agent':client.agent()}).text
        log(result)
        curl = re.findall('curl\s*=\s*[\"\']([^\"\']+)',result)[0]
        url = base64.b64decode(curl)
        token = json.loads(s.get('http://bro.adcast.tech/getToken.php').text)['token']
        url+=token

        url+='|%s' % urllib.urlencode({'User-agent':client.agent(),'Referer':ref,'X-Requested-With':constants.get_shockwave(),'Host':urlparse.urlparse(url).netloc})
        return url

    
    #except:
    #    return

