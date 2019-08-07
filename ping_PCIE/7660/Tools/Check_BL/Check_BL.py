import requests
import re
import os

setups = """
BEJSRTL442

BEJSRTL392

BEJSRTL738

BEJSRTL688

BEJSRTL749

BEJSRTL659 

BEJSRTL807

BEJSRTL853

BEJSRTL854

BEJSRTL738

BEJSRTL434

BEJSRTL688

BEJSRTL470

"""

setups = setups.strip().split()
##check FTP ping browsing
for i in setups:
    BL_link = 'http://' + i + '.bj.intel.com:8080/harts/current/'
    BL_link1 = 'http://' + i + '.bj.intel.com:8080/harts/config/cla/tc_flow_control.properties'
    BL_link2 = 'http://' + i + '.bj.intel.com:8080/harts/config/cla/cla.properties'

    flag = os.system('ping %s.bj.intel.com -n 1 > null' % i)
    if flag == 0:
        # baseline
        pattern = re.compile(r'>[t/b].+cfg')
        result = re.search(pattern, str(requests.get(BL_link).text)).group(0).strip('>')
        # platform
        pattern1 = re.compile(r'tccontrol.+PCIEFLASHLESS')
        result1 = re.findall(pattern1, str(requests.get(BL_link1).text))
        # FTP
        pattern2 = re.compile(r'psdata.ftpserver.address.+[0-9][0-9]')
        # Ping
        pattern3 = re.compile(r'psdata.pingserver.address.+[0-9][0-9]')
        # Browsing
        pattern4 = re.compile(r'psdata.browsingserver.address.+[0-9][0-9]')
        #sim0
        pattern5 = re.compile(r'simsetting.testmobile.sim1.networkoperator=.+[c,C]')
        pattern6 = re.compile(r'simsetting.refmobile.mobilenumber=.+[0-9]')
        #username password
        pattern7 = re.compile(r'psdata.ftpserver.username=IntelFTP')
        pattern8 = re.compile(r'psdata.ftpserver.passwd=intel@123')
        pattern9 = re.compile(r'imc.+[0-9]/"')
        pattern10 = re.compile(r'simsetting.testmobile.sim1.mobilenumber=.+[0-9]')
        pattern11 = re.compile(r'simsetting.testmobile.sim2.mobilenumber=.+[0-9]')
        pattern12 = re.compile(r'simsetting.refmobile.mobilenumber=.+[0-9]')
        pattern13 = re.compile(r'simsetting.refmobile2.mobilenumber=.+[0-9]')
        pattern14 = re.compile(r'imc.+[0-9]')
        if re.search(pattern2, str(requests.get(BL_link2).text)) is None:
            result2 = re.search(pattern2, str(requests.get(BL_link2).text))
        else:
            result2 = re.search(pattern2, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern3, str(requests.get(BL_link2).text)) is None:
            result3 = re.search(pattern3, str(requests.get(BL_link2).text))
        else:
            result3 = re.search(pattern3, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern4, str(requests.get(BL_link2).text)) is None:
            result4 = re.search(pattern4, str(requests.get(BL_link2).text))
        else:
            result4 = re.search(pattern4, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        # result5 = re.search(pattern5, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        result6 = re.search(pattern6, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern7, str(requests.get(BL_link2).text)) is None:
            result7 = re.search(pattern7, str(requests.get(BL_link2).text))
        else:
            result7 = re.search(pattern7, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern8, str(requests.get(BL_link2).text)) is None:
            result8 = re.search(pattern8, str(requests.get(BL_link2).text))
        else:
            result8 = re.search(pattern8, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern9, str(requests.get(BL_link).text)) is None:
            result9 = re.search(pattern9, str(requests.get(BL_link).text))
        else:
            result9 = re.search(pattern9, str(requests.get(BL_link).text)).group(0).split('/')[0]
        result10 = re.search(pattern10, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern11, str(requests.get(BL_link2).text)) is None:
            result11 = re.search(pattern11, str(requests.get(BL_link2).text))
        else:
            result11 = re.search(pattern11, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        result12 = re.search(pattern12, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        if re.search(pattern13, str(requests.get(BL_link2).text)) is None:
            result13 = re.search(pattern13, str(requests.get(BL_link2).text))
        else:
            result13 = re.search(pattern13, str(requests.get(BL_link2).text)).group(0).split('=')[1]
        # BEJSRTL730 	 b190704_L7660-mtbf-sit-gnss.cfg
        # print(i, '\t', result)
        # BEJSRTL730 	 tccontrol28.value=ICE7660MK2PCIEFLASHLESS 	 tccontrol31.value=ICE7660MK2PCIEFLASHLESS
        # print(i, '\t', result1[0], '\t', result1[1])
        # BEJSRTL773 	 112.35.30.117 	 112.35.30.117 	 112.35.30.117 	 IntelFTP 	 intel@123
        # print(i, '\t', result2, '\t', result3, '\t', result4, '\t', result7,  '\t', result8)
        # BEJSRTL773 	 CTC 	 53930024
        # print(i, '\t', result5, '\t', result6)
        # BEJSRTL021      imc_ipc_1A_V7.10.03
        # print(i, '\t', result9)
        # BEJSRTL773 	 +8618911175664 	 None
        print(i, '\t', result10, '\t', result11)
        # print(i, '\t', result12, '\t', result13)
    else:
        # content = BeautifulSoup(requests.get(BL_link).text, 'lxml')
        # key = content.find_all(title='Network Error')
        # print(key)
        print(i, '\t', 'Check by manual!')

##modify FTP ping browsing
