import configparser
from selenium import webdriver
import threading
import time
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import  By


class MyFounctionData:

    def read_rack_name(self, section):
        name_list = configparser.ConfigParser()
        name_list.read("C:\zxq\\\\7660\Tools\selenium\config\\racks_list.ini")
        name_list.get(section, "name")
        return name_list.get(section, "name")


class MyFounction:

    def __init__(self, rack):
        self.driver = webdriver.Chrome()
        self.rack = rack
        self.url = "https://oc6web-harts.intel.com/integfe/node/details/" + rack + ".BJ.INTEL.COM"
        self.driver.get(self.url)
        self.driver.maximize_window()

    def open_url(self):
        self.login()
        self.find_abort_button()
        # time.sleep(5)
        # tables = self.driver.find_element_by_class_name("btn-danger").text
        # print(tables)

    def find_abort_button(self):
        self.exception_by_class_name("btn-danger")
        self.driver.close()

    def login(self):
        self.exception_by_name("username")
        self.driver.find_element_by_name("username").send_keys("CCR\\xiaoqi4x")
        self.driver.find_element_by_name("password").send_keys("890@intel")
        self.driver.find_element_by_xpath("/html/body/app-root/div/div[2]/div/div[1]/div[2]/form/div[4]/div/button").click()

    def exception_by_name(self, name):
        loop = 0
        while loop == 0:
            try:
                self.driver.find_element_by_name(name)
            except:
                loop = 0
                print(loop)
            else:
                loop = 1
                print("find name")

    def exception_by_class_name(self, class_name):
        loop = 0
        while loop == 0:
            try:
                self.driver.find_element_by_class_name(class_name)
            except:
                loop = 0
                print("0")
            else:
                loop = 1
                print("find class name")


class MyThread(threading.Thread):

    def __init__(self, rack):
        threading.Thread.__init__(self)
        self.rack = rack

    def run(self):
        mf = MyFounction(self.rack)
        mf.open_url()


section_choose = input("please input which u want to stop:")
mfd = MyFounctionData()
thread_list = []
for i in mfd.read_rack_name(section_choose).split(','):
    thread = MyThread(i)
    thread.start()
    thread_list.append(thread)

for i in thread_list:
    i.join()

