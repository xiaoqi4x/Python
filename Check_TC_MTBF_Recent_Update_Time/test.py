import requests
from urllib import request

from bs4 import BeautifulSoup
ver = "http://harts.intel.com/harts6/ListTestsets.do?slaveName=BEJSRTL351.bj.intel.com"
ver1 = "https://harts.intel.com/harts6/ListTestsets.do?slaveName=BEJSRTL662.bj.intel.com"
print(requests.get(ver1,verify=False).status_code)
url = "http://bejsrtl662.bj.intel.com:8080/harts/logs/test_sets//57204306/test_engine/MTBF_RELEASE_TEST_7660.xml_20181222072342/"

result = requests.get(url + 'campaign_start.txt', verify=_verify).text
print(result)
#content = page.read()
#content1 = content.decode('utf-8')
#print(BeautifulSoup(content1, 'html.parser'))