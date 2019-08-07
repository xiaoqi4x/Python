import requests
import re
BL_link = 'http://bejsrtl747.bj.intel.com:8080/harts/current/'
if requests.get(BL_link).status_code == 200:
    pattern = re.compile(r'>b.+cfg')
    result = re.search(pattern,str(requests.get(BL_link).text)).group(0).strip('>')
    #print(str(requests.get(BL_link).text))
    print(result)