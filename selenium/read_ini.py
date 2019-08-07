import configparser
cf = configparser.ConfigParser()
cf.read("C:\zxq\\\\7660\Tools\selenium\config\localElement.ini")

print(type(cf.get('element', 'user_email')))
print(cf.get('element', 'user_email').split(":")[1])


