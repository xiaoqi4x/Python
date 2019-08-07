import requests
import threading
import urllib3
import json
import re
import subprocess
import paramiko


class MyThread(threading.Thread):
    def __init__(self, i):
        threading.Thread.__init__(self)
        self.i = i
        self.information = {}

    def get_result(self):
        return self.information

    def run(self):
        self.information = {'rack': self.i, 'baseline': '-', 'platform': '-', 'FTP': '-', 'username': '-',
                            'password': '-',
                            'ping': '-', 'browsing': '-', 'sim0_operator': '-',
                            'sim0_num': '-', 'sim0_ref': '-',  'sim1_operator': '-','sim1_num': '-', 'sim1_ref': '-'}
        BL_link = 'http://' + self.i + '.bj.intel.com:8080/harts/current/'
        BL_link1 = 'http://' + self.i + '.bj.intel.com:8080/harts/config/cla/tc_flow_control.properties'
        BL_link2 = 'http://' + self.i + '.bj.intel.com:8080/harts/config/cla/cla.properties'
        # flag = os.system('ping %s.bj.intel.com -n 1 > null' % self.i)
        flag = requests.get(BL_link).status_code
        if flag == 200:
            # baseline
            pattern = re.compile(r'>[t/b].+cfg')
            self.information['baseline'] = re.search(pattern, str(requests.get(BL_link).text)).group(0).strip('>')
            # platform
            pattern1 = re.compile(r'tccontrol.+PCIEFLASHLESS')
            self.information['platform'] = re.findall(pattern1, str(requests.get(BL_link1).text))
            if len(self.information['platform']) == 2 and self.information['platform'][0] == \
                    self.information['platform'][0]:
                self.information['platform'] = 'ICE7660PCIEFLASHLESS'
            elif len(self.information['platform']) == 1:
                self.information['platform'] = self.information['platform'][0].split('=')[1]
            # FTP
            pattern2 = re.compile(r'psdata.ftpserver.address.+[0-9][0-9]')
            # Ping
            pattern3 = re.compile(r'psdata.pingserver.address.+[0-9][0-9]')
            # Browsing
            pattern4 = re.compile(r'psdata.browsingserver.address.+[0-9][0-9]')
            # sim0 is cuc
            pattern5 = re.compile(r'simsetting.testmobile.sim1.networkoperator=.+[c,C,R,E,i]')
            pattern6 = re.compile(r'simsetting.testmobile.sim2.networkoperator=.+[c,C,R,E,i]')
            # username password
            pattern7 = re.compile(r'psdata.ftpserver.username=IntelFTP')
            pattern8 = re.compile(r'psdata.ftpserver.passwd=intel@123')
            pattern10 = re.compile(r'simsetting.testmobile.sim1.mobilenumber=.+[0-9]')
            pattern11 = re.compile(r'simsetting.testmobile.sim2.mobilenumber=.+[0-9]')
            pattern12 = re.compile(r'simsetting.refmobile.mobilenumber=.+[0-9]')
            pattern13 = re.compile(r'simsetting.refmobile2.mobilenumber=.+[0-9]')
            if re.search(pattern2, str(requests.get(BL_link2).text)) is None:
                self.information['FTP'] = re.search(pattern2, str(requests.get(BL_link2).text))
            else:
                self.information['FTP'] = re.search(pattern2, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            if re.search(pattern3, str(requests.get(BL_link2).text)) is None:
                self.information['ping'] = re.search(pattern3, str(requests.get(BL_link2).text))
            else:
                self.information['ping'] = re.search(pattern3, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            if re.search(pattern4, str(requests.get(BL_link2).text)) is None:
                self.information['browsing'] = re.search(pattern4, str(requests.get(BL_link2).text))
            else:
                self.information['browsing'] = \
                re.search(pattern4, str(requests.get(BL_link2).text)).group(0).split('=')[
                    1]
            self.information['sim0_operator'] = \
                re.search(pattern5, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            if re.search(pattern6, str(requests.get(BL_link2).text)) is None:
                self.information['sim1_operator'] = re.search(pattern6, str(requests.get(BL_link2).text))
            else:
                self.information['sim1_operator'] = \
                    re.search(pattern5, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            if re.search(pattern7, str(requests.get(BL_link2).text)) is None:
                self.information['username'] = re.search(pattern7, str(requests.get(BL_link2).text))
            else:
                self.information['username'] = \
                re.search(pattern7, str(requests.get(BL_link2).text)).group(0).split('=')[
                    1]
            if re.search(pattern8, str(requests.get(BL_link2).text)) is None:
                self.information['password'] = re.search(pattern8, str(requests.get(BL_link2).text))
            else:
                self.information['password'] = \
                re.search(pattern8, str(requests.get(BL_link2).text)).group(0).split('=')[
                    1]
            self.information['sim0_num'] = re.search(pattern10, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            if re.search(pattern11, str(requests.get(BL_link2).text)) is None:
                self.information['sim1_num'] = re.search(pattern11, str(requests.get(BL_link2).text))
            else:
                self.information['sim1_num'] = \
                    re.search(pattern11, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            self.information['sim0_ref'] = re.search(pattern12, str(requests.get(BL_link2).text)).group(0).split('=')[1]
            if re.search(pattern13, str(requests.get(BL_link2).text)) is None:
                self.information['sim1_ref'] = re.search(pattern13, str(requests.get(BL_link2).text))
            else:
                self.information['sim1_ref'] = \
                    re.search(pattern13, str(requests.get(BL_link2).text)).group(0).split('=')[1]


class MyThread1(threading.Thread):
    def __init__(self, section, rack):
        threading.Thread.__init__(self)
        self.section = section
        self.rack = rack+'.bj.intel.com'
        self.information = {}

    def get_result(self):
        return self.information

    def run(self):
        self.information = {'SECTION': self.section, 'RACK': self.rack.split('.')[0], 'Campaign_ID': '-', 'VER': '-', 'STATUS': '-',
                            'Update_Time': '-', 'Data_Pre': '-', 'ICE_new_sequence': '-', 'ABCC': '-', 'Audio_Interface': '-', 'Audio_test': '-', 'Operate0': '-',
                            'Operate1': '-', 'VOLTE': '-', 'VSWR': '-', 'CDMA': '-', 'Build': '-', 'Variant': '-'}
        # if requests.get('http://' + self.rack + '.bj.intel.com:8080/harts/').status_code == 200:
        if subprocess.call('ping -n 1 %s' %self.rack, shell=True, stdout=subprocess.PIPE) == 0:
            url = 'https://harts.intel.com/hcloud/bews/v1/campaign/report?count=5&format=JSON&node=' + self.rack + '&offset=0'
            urllib3.disable_warnings()
            result = requests.get(url, verify=False).text
            result = json.loads(result)
            if result['response']['itemList'][1]['status'] == "TESTING":
                self.information['STATUS'] = result['response']['itemList'][1]['status']
                self.information['Campaign_ID'] = result['response']['itemList'][1]['id']
                self.information['VER'] = str(result['response']['itemList'][1]['name']).split('_')[5]
            else:
                self.information['STATUS'] = result['response']['itemList'][0]['status']
                self.information['Campaign_ID'] = result['response']['itemList'][0]['id']
                self.information['VER'] = str(result['response']['itemList'][0]['name']).split('_')[5]
            log_link = 'http://' + self.rack + ':8080/harts/logs/test_sets/' + str(
                    self.information['Campaign_ID']) + '/test_engine/'
            result1 = requests.get(log_link, verify=False).text
            pattern = re.compile(r'MTBF_RELEASE_TEST_7660.+?/')
            mtbf_folder = re.search(pattern, result1)
            if mtbf_folder is None:
                self.information['Update_Time'] = self.information['Build'] = self.information['Variant'] = 'None'
            else:
                self.information['Update_Time'] = MyFounctions(log_link + mtbf_folder.group(0)).update_time()
                self.information['Build'] = MyFounctions(log_link + mtbf_folder.group(0)).build()
                self.information['Variant'] = MyFounctions(log_link + mtbf_folder.group(0)).variant()
            #     #define url
            hmt_url = 'http://' + self.rack + ':8080/harts/resources/test_sets/' + str(self.information[
                'Campaign_ID']) + '/campaigns/MTBF_RELEASE_TEST_7660.xml.xml'
            hmt_url1 = 'http://' + self.rack + ':8080/harts/resources/test_sets/' + str(self.information[
                'Campaign_ID']) + '/config/tc_flow_control.properties'
            hmt_result = requests.get(hmt_url, verify=False).text
            hmt_result1 = requests.get(hmt_url1, verify=False).text
            # pattern
            pattern_data_pre = re.compile(r'SIM_TO_REMOVE_DATA_TESTS_FROM" value=.+?"')
            pattern_ice_new_seq = re.compile(r'TCMTBF_ICE_NEW_SEQUENCE" value=.+?"')
            pattern_abcc = re.compile(r'ABCC_STATE_TO_SET" value=.+?"')
            pattern_audio_interface = re.compile(r'ACTIVE_AUDIO_INTERFACE" value=.+?"')
            pattern_audio_test = re.compile(r'RUN_AUDIO_TESTS" value=.+?"')
            pattern_op0 = re.compile(r'tccontrol.+DesiredRATSIM0')
            pattern_op1 = re.compile(r'tccontrol.+DesiredRATSIM1')
            pattern_volte = re.compile(r'tccontrol.+ENABLE_VOLTE')
            pattern_vswr= re.compile(r'tccontrol.+TCMTBF_VSWR')
            pattern_cdma = re.compile(r'tccontrol1.+ENABLE_CDMA_SUPPORT')
            op0_num = re.search(pattern_op0, hmt_result1).group(0).split('.')[0]
            op1_num = re.search(pattern_op1, hmt_result1).group(0).split('.')[0]
            pattern_volte_num = re.search(pattern_volte, hmt_result1).group(0).split('.')[0]
            pattern_vswr_num = re.search(pattern_vswr, hmt_result1).group(0).split('.')[0]
            pattern_cdma_num = re.search(pattern_cdma, hmt_result1).group(0).split('.')[0]
            pattern_op0_value = re.compile(r'%s.value=.+'% op0_num)
            pattern_op1_value = re.compile(r'%s.value=.*'% op1_num)
            pattern_volte_value = re.compile(r'%s.value=.*'% pattern_volte_num)
            pattern_vswr_value = re.compile(r'%s.value=.*'% pattern_vswr_num)
            pattern_cdma_value = re.compile(r'%s.value=.*'% pattern_cdma_num)
            self.information['Data_Pre'] = re.search(pattern_data_pre, hmt_result).group(0).split('=')[1].strip('"')
            self.information['ICE_new_sequence'] = re.search(pattern_ice_new_seq, hmt_result).group(0).split('=')[1].strip('"')
            self.information['ABCC'] = re.search(pattern_abcc, hmt_result).group(0).split('=')[1].strip('"')
            self.information['Audio_Interface'] = re.search(pattern_audio_interface, hmt_result).group(0).split('=')[1].strip('"')
            self.information['Audio_test'] = re.search(pattern_audio_test, hmt_result).group(0).split('=')[1].strip('"')
            self.information['Operate0'] = re.search(pattern_op0_value, hmt_result1).group(0).split('=')[1]
            if re.search(pattern_op1_value, hmt_result1).group(0).split('=')[1] == '':
                self.information['Operate1'] = 'N/A'
            else:
                self.information['Operate1'] = re.search(pattern_op1_value, hmt_result1).group(0).split('=')[1]
            if re.search(pattern_volte_value, hmt_result1).group(0).split('=')[1] == '' or re.search(pattern_volte_value, hmt_result1).group(0).split('=')[1] == 'NONE':
                self.information['VOLTE'] = '-'
            else:
                self.information['VOLTE'] = re.search(pattern_volte_value, hmt_result1).group(0).split('=')[1]
            self.information['VSWR'] = re.search(pattern_vswr_value, hmt_result1).group(0).split('=')[1]
            if re.search(pattern_cdma_value, hmt_result1).group(0).split('=')[1] =='':
                self.information['CDMA'] = 'false'
            else:
                self.information['CDMA'] = re.search(pattern_cdma_value, hmt_result1).group(0).split('=')[1]
        else:
            self.information['STATUS'] = 'PC_DOWN'


class MyThread2(threading.Thread):
    def __init__(self, mac):
        threading.Thread.__init__(self)
        self.mac = mac + '.bj.intel.com'
        self.disk = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

    def get_result(self):
        return self.disk

    def get_mac(self):
        return self.mac.split('.')[0]

    def run(self):
        if subprocess.call('ping -n 1 %s' % self.mac, shell=True, stdout=subprocess.PIPE) == 0:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.mac, 22, 'hcloud', 'Intel1234!')
            stdin, stdout, stderr = ssh.exec_command('df -h')
            result = stdout.read().decode(encoding='utf-8')
            for i in result.split('\n'):
                if i[-1:] == '/':
                    self.disk = i.split()
                    self.disk.append('ok')
                    break
        else:
            self.disk.append('failed')
        return self.disk



class MyFounctions:

    def __init__(self, log_link):
        self.log_link = log_link

    def update_time(self):
        result1 = requests.get(url=self.log_link, verify=False).text
        pattern1 = re.compile(r'TC_MTBF_7660_.+?/')
        TC_MTBF_folder = pattern1.search(result1)
        if TC_MTBF_folder is None:
            return 0
        else:
            time_stamp = []
            log_link_2 = self.log_link + '/' + TC_MTBF_folder.group(0)
            result2 = requests.get(log_link_2, verify=False).text
            pattern2 = re.compile(r'/">TC_MTBF_7660.+?  <')
            log_folder = pattern2.findall(result2)
            if len(log_folder) > 0:
                for i in log_folder:
                    time_stamp.append(str(i).split('"')[3].lstrip('>').rstrip('  <'))
                    update_time = sorted(time_stamp)[-1]
                return update_time
            else:
                return 0

    def variant(self):
        result = requests.get(url=self.log_link, verify=False).text
        pattern = re.compile(r'[A-Z].+_TC_100_2_0_BootAndATCheck.+?/')
        at_boot = pattern.search(result)
        if at_boot is None:
            return 'None'
        else:
            at_boot_path = self.log_link + at_boot.group(0).split('>')[1] + 'TC_100_2_0_BootAndATCheck.txt'
            at_boot_content = requests.get(at_boot_path, verify=False).text
            pattern1 = re.compile(r'ICE7660_XMM7660_RFDEV.+[S,R]')
            variant = pattern1.search(at_boot_content)
            if variant is None:
                return 'None'
            else:
                return variant.group(0)

    def build(self):
        result = requests.get(url=self.log_link, verify=False).text
        pattern = re.compile(r'[P,F].+_TC_100_2_0_BootAndATCheck.+?/')
        at_boot = pattern.search(result)
        if at_boot is None:
            return 'None'
        else:
            at_boot_path = self.log_link + at_boot.group(0).split('>')[1] + 'TC_100_2_0_BootAndATCheck.txt'
            at_boot_content = requests.get(at_boot_path, verify=False).text
            pattern1 = re.compile(r'[0-9]__.+"')
            build = pattern1.search(at_boot_content)
            if build is None:
                return 'None'
            else:
                return build.group(0)[3:-2]




class TestFounction:

    def test(self):
        rack = 'bejsrtm005smini'
        disk =  []
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(rack, 22, 'hcloud', 'Intel1234!')
        stdin, stdout, stderr = ssh.exec_command('df -h')
        result = stdout.read().decode(encoding='utf-8')
        if subprocess.call('ping -n 1 %s' %rack, shell=True, stdout=subprocess.PIPE) == 0:
            for i in result.split('\n'):
                if i[-1:] == '/':
                    disk = i.split()
                    disk.append('ok')
                    print(disk)
                    break
        else:
            return 'failed'

#
# a = TestFounction()
# a.test()


