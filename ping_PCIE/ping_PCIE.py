import os
import csv
# if ping is ok, return 0, else return 1
number = 0
print('Please waiting..........\n')
with open('7660rackName.csv') as csvfile:
    csv_reader=csv.reader(csvfile)
    for rackName in csv_reader:
        if os.system('ping -n 2 %s > null' % rackName[0]) == 0:
            continue
        else:
            print(rackName[0])
            number = number + 1
if number == 0:
    print('Congradulations!!! No rack check cannot be ping successfully!!!')
else:
    print('\nSorry!!! above racks cannot be ping successfully!!! ')