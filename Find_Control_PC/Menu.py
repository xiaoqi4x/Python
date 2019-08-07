#C:\zxq\Find_Control_PC
import csv
import time
csv_file = csv.reader(open('IBISControlPC.csv', 'r'))
rack=input('please input rack name:')
i = 0
for infor in csv_file:
    if infor[1] == rack:
        print(infor[0])
        time.sleep(3)
        i = 1
        break
if i == 0:
    print('No this rack!!')
    time.sleep(3)
