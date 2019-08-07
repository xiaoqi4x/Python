from urllib import request
import csv
# if ping is ok, return 0, else return 1
number = 0
key = "(abort)"
print('Please waiting..........\n')
with open('7660HMTLink.csv') as csvfile:
    csv_reader = csv.reader(csvfile)
    for rackName in csv_reader:
        page = request.urlopen(rackName[0])
        content = page.read()
        content1 = content.decode('utf-8')
        if key in content1:
            continue
        else:
            print(rackName[0][-23:-13] + ' is not running ---' + rackName[1])
            number = number + 1
if number == 0:
    print('Congradulations!!! All rack are running!!!')
else:
    print('\nSorry!!! above racks stopped!!! ')


