from bs4 import BeautifulSoup
from conf import setting
from machine import Machine

import re
import requests
import openpyxl
import threading
import time
import webbrowser

pattern_build = re.compile('SWVERSION.+\n.+', flags=re.MULTILINE)  # 匹配build

pattern_sim0_rat = re.compile("Initial RAT for testing is configured as ...(.+)\[MTBF")  # 匹配HMT rat0
pattern_sim1_rat = re.compile("Is Multi-RAT configured for this campaign\?(.+)\[MTBF")  # 匹配HMT rat1
pattern_HMT = re.compile(r"TC version: hcloud_modem_tests-(.+?)<")  # 匹配HMT version
pattern_volte = re.compile('ENABLE_VOLTE .+? source: tcf_config, value:(\s*[\d|\w]+)')  # 匹配volte
pattern_crash = re.compile(r'CORE_DUMP_.+?txt')
pattern_reset = re.compile(r'BB_RESET_.+?txt')
pattern_imie = re.compile(r"tccontrol14.value=(.+)")


class MTBF_tool(object):

    def __init__(self):
        self.thread_list = []  # 记录线程
        self.lock = threading.Lock()  # 申明线程锁
        self.setup_info = {}  # setup info

    @staticmethod
    def get_webpage(url):
        soup = None
        try:
            page = requests.get(url, timeout=10)  # get url content
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
        except Exception as e:
            print('url', url)
            print('\033[1;31mException:%s.\033[0m' % e)
        return soup

    def check_testing_para(self, machine_obj, tag):
        machine_obj.harts['log_num'] = re.search(r"'\d+'", str(tag)).group()
        machine_obj.harts['ver_id'] = re.search(r"(\d\d+)", str(tag.find_previous_sibling())).group(1)
        machine_obj.test_engine_url = 'http://%s.%s:8080/harts/logs/test_sets/%s/test_engine/' % \
                                      (machine_obj.name, setting.SITE_HARTS[''.join(machine_obj.name[0:3])],
                                       machine_obj.harts['log_num'].strip("'"))
        return 0

    def check_testing(self, machine_obj):
        soup = self.get_webpage(machine_obj.harts_node)
        # url: http://harts.intel.com/harts6/ListTestsets.do?slaveName=BEJSRTL256.BJ.INTEL.COM
        if soup:
            testing_state = soup.find_all(class_='abort')
            if len(testing_state) == 1:
                machine_obj.harts['state'] = 'testing'
                self.check_testing_para(machine_obj, testing_state[0])
            elif len(testing_state) > 1:
                machine_obj.harts['state'] = 'pending exist'
                queue_id = ''
                for test in testing_state:
                    test_state = test.find_parent().find_parent().find_next_sibling().find_next_sibling().find(
                        class_="siSmlTxt").text
                    if str(test_state) == 'Testing':
                        self.check_testing_para(machine_obj, test)
                    else:
                        queue_id = queue_id + '_' + str(
                            re.search(r"(\d\d+)", str(test.find_previous_sibling())).group(1))
                machine_obj.harts['ver_id'] += queue_id
            else:
                machine_obj.harts['state'] = 'completed'
                machine_obj.hmt = None
                machine_obj.sim0_rat = ''
                machine_obj.current_iteration_log_time = None
        return 0

    @staticmethod
    def check_connection(machine_obj):
        """
        check network connection: ok/failed
        :param machine_obj:
        :return:
        """
        try:
            page = requests.get(machine_obj.config_path, timeout=10)  # get url content
            if page.status_code == 200:
                machine_obj.connection = 'ok'
            else:
                machine_obj.connection = 'failed'
        except Exception as e:
            print('url', machine_obj.config_path)
            print('\033[1;31mException:%s.\033[0m' % e)

    def check_test_engine(self, machine_obj):
        "url: http://bejsrtl364.bj.intel.com:8080/harts/logs/test_sets/56739522/test_engine/"
        soup = self.get_webpage(machine_obj.test_engine_url)
        if soup:
            tags = soup.find_all(text=re.compile('MTBF_RELEASE_TEST.*'))
            time = 0
            for tag in tags:
                time1 = str(tag).split('_')[-1].strip('/')
                if str(time1) > str(time):
                    machine_obj.test_engine_folder = tag.strip('/')
            if machine_obj.test_engine_folder:
                machine_obj.prelog_url = '%s/%s' \
                                         % (machine_obj.test_engine_url, machine_obj.test_engine_folder)
        return 0

    def check_test_issue(self, machine_obj):
        "url: http://bejsrtl364.bj.intel.com:8080/harts/logs/test_sets/56739522/test_engine/MTBF_RELEASE_TEST_20181214030518/"
        prepare_path = None
        tc = None
        soup = self.get_webpage(machine_obj.prelog_url)
        if soup:
            machine_obj.crash = len(soup.find_all(text=re.compile('CORE_DUMP_.+?txt')))
            machine_obj.reset = len(soup.find_all(text=re.compile('BB_RESET_.+?txt')))
            prepare_path = soup.find(text=re.compile('COMBI_TC_MTBF_Prepare_Device'))
            tc = soup.find(text=re.compile('^TC_MTBF_.*'))
        if prepare_path:
            machine_obj.prepare_url = "%s/%sCOMBI_TC_MTBF_Prepare_Device.txt" % (machine_obj.prelog_url, prepare_path)
        if tc:
            machine_obj.tcmtbf_url = '%s/%s' % (machine_obj.prelog_url, tc)
        return 0

    @staticmethod
    def check_prepare(obj):
        try:
            result = requests.get(url=obj.prepare_url, timeout=15)
            if result.status_code == 200:
                result = result.text
                build = re.search(pattern_build, str(result))
                rat0 = re.search(pattern_sim0_rat, str(result))
                rat1 = re.search(pattern_sim1_rat, str(result))
                hmt = re.search(pattern_HMT, str(result))
                volte = re.search(pattern_volte, str(result))
                if build:
                    obj.build = build.group(0).split('*')[1].split("__", 1)[1]
                if rat0:
                    obj.sim0_rat = rat0.group(1).strip()
                if rat1:
                    if rat1.group(1).strip() == 'true':
                        obj.sim0_rat = 'MULTI_RAT'
                if hmt:
                    obj.hmt = hmt.group(1)
                if volte:
                    obj.volte = volte.group(1)
        except Exception as e:
            print(e)

    def check_tc_mtbf(self, obj):
        soup = self.get_webpage(obj.tcmtbf_url)
        if soup:
            tc_iteration_log = soup.find_all('td', text=re.compile('^TC_MTBF_.+'))
            tag_time = []
            for i in tc_iteration_log:
                tag_time.append(next(i.next_siblings).text)
            try:
                obj.current_iteration_log_time = sorted(tag_time)[-1]  # latest update time
            except Exception as e:
                obj.current_iteration_log_time = 'no log update'

    def html_dis(self, csv_name):
        s = ''
        tab1 = """
                <table>
                <thead>
                <tr style="height:25px;background-color: #bee6e3">
                    <td>section</td>
                    <td>setup</td>
                    <td>datatime</td>
                </tr>
                </thead>
                <tbody>
                <tr>
                    <td>{h_section}</td>
                    <td>{h_setup}</td>
                    <td>{h_datatime}</td>
                        </tr>
                        </tbody>
                    </table>
                    """.format(h_section=csv_name, h_setup=len(self.setup_info[csv_name]),
                               h_datatime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        tab2_head = """
                <tr style="height:25px;background-color: #bee6e3">
                    <td>machine</td>
                    <td>state</td>
                    <td>connection</td>
                    <td>operator</td>
                    <td>RAT</td>
                    <td>volte</td>
                    <td>crash</td>
                    <td>reset</td>
                    <td>hmt</td>
                    <td>latest_update_time</td>
                    <td>build</td>
                </tr>     
        """
        for machine in self.setup_info[csv_name]:
            s1 = """
                <tr>
                    <td><a href='http://harts.intel.com/harts6/ListTestsets.do?slaveName={name_harts}.BJ.INTEL.COM' target="_blank">{name}</td>
                    <td>{state}</td>
                    <td>{connection}</td>
                    <td>{operator}</td>
                    <td>{RAT}</td>
                    <td>{volte}</td>
                    <td>{crash}</td>
                    <td>{reset}</td>
                    <td>{hmt}</td>
                    <td>{latest_update_time}</td>
                    <td>{build}</td>
                <tr>

            """.format(name_harts=machine.name, name=machine.name, state=machine.harts['state'],
                       connection=machine.connection,
                       operator=machine.operator, RAT=machine.sim0_rat + machine.sim1_rat,
                       volte=machine.volte, crash=machine.crash, reset=machine.reset, hmt=machine.hmt,
                       latest_update_time=machine.current_iteration_log_time, build=machine.build)
            s = s + s1
        with open(r"D:\Program\myMTBF\mymtbf\static/ml_%s.html" % csv_name, 'r', encoding='utf-8') as f_html:
            data = str(f_html.read())
            data = data % (csv_name, tab1, tab2_head, s)
        with open(r"D:\Program\myMTBF\mymtbf\templates/%s.html" % csv_name, 'w', encoding='utf-8') as f:
            f.write(data)

    def mtbf_test(self, machine_obj, section):
        machine = machine_obj.name
        self.check_testing(machine_obj)
        while True:
            self.check_connection(machine_obj)
            if machine_obj.harts['state'].strip() == 'completed':
                break
            self.check_test_engine(machine_obj)
            if not machine_obj.prelog_url:
                break
            self.check_test_issue(machine_obj)
            if not machine_obj.prepare_url:
                break
            if not (machine_obj.hmt and machine_obj.sim0_rat and machine_obj.build):
                pass
            self.check_prepare(machine_obj)
            if not machine_obj.tcmtbf_url:
                break
            self.check_tc_mtbf(machine_obj)
            break

    def execute_mtbf(self, machine_obj, section):
        t = threading.Thread(target=self.mtbf_test, args=(machine_obj, section))
        t.start()
        self.thread_list.append(t)  # add current thread into thread list

    def execute(self):
        db = setting.DB['7560']  # select database
        try:
            wb = openpyxl.load_workbook(db)  # load workbook
            sheets = ['PRE', 'SUTC', 'MUTC', 'SCR', 'MICE']
            sheets = ['SUTC', 'MUTC','MICE','PRE']
            while True:  # loop csv_name
                for csv_name in sheets:
                    ws = wb[csv_name]  # get worksheet obj
                    t1 = time.time()
                    if csv_name not in self.setup_info:
                        self.setup_info[csv_name] = []  # record setup obj
                        for row in ws.iter_rows(min_row=2):  # iterate worksheet with row ways
                            machine_obj = Machine(row[0].value.strip())  # instantiate Machine obj
                            machine_obj.operator = row[1].value.strip()
                            self.setup_info[csv_name].append(machine_obj)  # append machine obj into to  setup_info list
                            self.execute_mtbf(machine_obj, csv_name)
                    else:
                        for machine in self.setup_info[csv_name]:
                            self.execute_mtbf(machine, csv_name)
                    for t in self.thread_list:
                        t.join()
                    self.html_dis(csv_name)
                    print('[%s]' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'total setup:',
                          len(self.setup_info[csv_name]))  # print total setup
                    print('[%s]' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'time', time.time() - t1)

        except Exception as e:
            print('\033[1;31mException:%s.\033[0m' % e)


def main():
    """
    tool entry
    :return:
    """
    mtbf = MTBF_tool()  # instantiate mtbf obj
    mtbf.execute()  # execute obj function



