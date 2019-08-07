class JudgeHuiWen:

    def huiwen(self):
        number = input("please input the number which u want to judge:")
        number_list = list(number)
        number_list.reverse()
        new_number = ''.join(number_list)
        if number == new_number:
            print(number + " is huiwenshu")
        else:
            print(number + " is not huiwenshu")


result = JudgeHuiWen()
result.huiwen()
