from urllib import request
from bs4 import BeautifulSoup
import re
import requests
# sample:
# http://bejsrtl605.bj.intel.com:8080/harts/logs/test_sets//54198825/test_engine/MTBF_RELEASE_TEST_7660.xml_20181102071957/PASSED_FLASH_232763981805431/FLASH.txt
# <a class="abort" href="#" onclick="if(validateLogin()) performAbortAction('20180904_183921_ver_scheduler_186070_195121_1','51499931'); return false;">(abort)</a>
# str(tr_table[i]) sample:<td align="right">2018-09-05 15:38  </td>
# Control 75 Name : DesiredRATSIM0
# Control 75 Enabled : Yes
# Control 75 Value : TM_4G3G2G


class InformationCheck:

    #display wabpage content
    @staticmethod
    def webpage(url):
        page = request.urlopen(url)
        content = page.read()
        content1 = content.decode('utf-8')
        return BeautifulSoup(content1, 'html.parser')

    @staticmethod
    def sheet_name():
        pass




    @staticmethod
    def section_name():
        print('1: SSIM-ALL   2: SSIM-SEB   3: SSIM-UTC   4: MSIM-ALL   5: MSIM-SEB   6: MSIM-UTC   7: MSIM-B0')
        input_str = input("please input number which part u want to check:")
        csv_name = {'1': 'SSIM-ALL', '2': 'SSIM-SEB', '3': 'SSIM-UTC', '4': 'MSIM-ALL', '5': 'MSIM-SEB', '6': 'MSIM-UTC', '7': 'MSIM-B0'}
        try:
            csv_name[input_str]
        except KeyError:
            print("please input 1-8!")
        else:
            return csv_name[input_str]

    def check_mtbf_release_test_folder(self, url):
        if requests.get(url).status_code == 200:
            page_content = self.webpage(url)
            mtbf_release_test_folder_exist = page_content.find_all(text=re.compile('MTBF_RELEASE_TEST*'))
            return mtbf_release_test_folder_exist[0]
        else:
            return 'false'


    def check_baseline_from_campaign_start(self, url):
        if self.check_mtbf_release_test_folder(url) != 'false':
            result = requests.get(url + 'campaign_start.txt').text
            pattern_baseline = re.compile(r'Java\shome\sfolder:\s/harts/baselines/.+')
            baseline = re.search(pattern_baseline, str(result)).group(0).strip().strip('//')
            return baseline
        else:
            return 'false'

    def find_prepare_folder(self, url):
        if requests.get(url).status_code == 200:
            page_content = self.webpage(url)
            prepare_folder = page_content.find_all(text=re.compile('.?COMBI_TC_MTBF_Prepare_Device_.+'))
            if len(prepare_folder) > 0:
                return prepare_folder[0]
            else:
                return 'still no prepare folder!!!'

    def check_rat_combo_from_prepare(self, url):
        if requests.get(url).status_code == 200:
            if self.find_prepare_folder(url) != 'still no prepare folder!!!':
                if requests.get(url + self.find_prepare_folder(url)).status_code == 200:
                    result = requests.get(url + self.find_prepare_folder(url) + 'COMBI_TC_MTBF_Prepare_Device.txt').text
                    #Operator (CUC, CMCC)
                    #Operator (CUC)
                    #SIM0 rat: TM_4G3G2G
                    pattern_operator_sim0 = re.compile(r'Operator \(.+\)')
                    pattern_operator_sim1 = re.compile(r'Operator \(.+\)')
                    pattern_sim0 = re.compile(r'SIM0 rat:\s.+')
                    pattern_sim1 = re.compile(r'SIM1 rat:\s.+')
                    search_sim0 = re.search(pattern_sim0, str(result)).group(0)
                    search_sim1 = re.search(pattern_sim1, str(result))
                    search_sim0_operator = re.search(pattern_operator_sim0, str(result)).group(0).strip()
                    if search_sim1 is None:
                        rat_combo = search_sim0_operator.split(' ')[1].lstrip('(').rstrip(')') + ' ' + search_sim0.split(' ')[2] + ' ' + 'NA' + ' ' + 'NA'
                    else:
                        rat_combo = search_sim0_operator.split(' ')[1].lstrip('(').rstrip(',') + ' ' + search_sim0.split(' ')[2] + ' ' + \
                                    search_sim0_operator.split(' ')[2].rstrip(')') + ' ' + search_sim1.group(0).split(' ')[2]
                    return rat_combo
                else:
                    return 'false'
            else:
                return self.find_prepare_folder(url)
        else:
            return 'false'


    def check_build(self, url):
        result = requests.get(url=url).text
        pattern = re.compile(r"__...7660_.+")
        pattern1 = re.compile(r"/harts/baselines/.+mtbf")
        re_result = re.search(pattern, str(result))
        re_result1 = re.search(pattern1, str(result))
        if requests.get(url).status_code == 200:
            if re_result:
                #print(re_result1)
                return re_result.group(0)[2:-3]
            else:
                return 'check flash step!!!'
        else:
            return 'false'


    def output_flash_txt_link(self, url):
        if requests.get(url).status_code == 200:
            page_content = self.webpage(url)
            flash_folder = page_content.find_all(text=re.compile('.?FLASH_.+'))
            flash_folder1 = page_content.find_all(text=re.compile('.+BootAndATCheck_.+'))
            if len(flash_folder) > 0:
                return self.check_build(url + flash_folder[0] + 'FLASH.txt')
            elif len(flash_folder1) > 0:
                return self.check_build(url + flash_folder1[0] + 'TC_100_2_0_BootAndATCheck.txt')
            else:
                return 'still not flashing...'
        return 'false'


    def check_tc_mtbf_7660_txt(self, url):
        if requests.get(url).status_code == 200:
            page_content = self.webpage(url)
            tc_mtbf_folder = page_content.find_all(text=re.compile('^TC_MTBF_7660.+'))
            if len(tc_mtbf_folder) > 0:
                if '7660' in tc_mtbf_folder[0]:
                    txt = 'TC_MTBF_7660.txt'
                else:
                    txt = 'TC_MTBF.txt'
                tr_table = self.webpage(url + tc_mtbf_folder[0]).find_all('td')
                if len(tr_table) > 0:
                    for i in range(len(tr_table)):
                        if txt in str(tr_table[i]):
                            return str(tr_table[i + 1])[-23:-7]
                else:
                    return 'still in prepare stage!!!'
            else:
                return 'still in prepare stage!!!'
        else:
            return 'false'
