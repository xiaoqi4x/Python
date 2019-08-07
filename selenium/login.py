from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
import time
# from PIL import Image

"""identify a driver for Chrome"""
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://mail.qq.com/cgi-bin/loginpage")

"""swith to iframe because username in iframe"""
driver.switch_to_frame("login_frame")
locator = (By.ID, "u")

"""check which u need controls is exist in webpage"""
WebDriverWait(driver, 1).until(EC.visibility_of_element_located(locator))
driver.find_element_by_id("u").send_keys("1026756571@qq.com")
driver.find_element_by_id("p").send_keys("qwerty")

""""check the value is same as u input"""
#print(driver.find_element_by_id("p").get_attribute('value'))

""""shotcut verification code"""
# driver.save_screenshot("D:/xx.png")
# code_element = driver.find_element_by_id("verfy_code")
# left = code_element.location['x']
# top = code_element.location['y']
# right = code_element.size['width'] + left
# height = code_element.size['height'] + top
# im = Image.open("D:/xx.png")
# img = im.crop((left,top,right,height))
# img.save(""D:/xx-1.png"")

"""switch webpage from iframe to default"""
driver.find_element_by_id("login_button").click()
driver.switch_to_default_content()
time.sleep(10)
driver.close()





