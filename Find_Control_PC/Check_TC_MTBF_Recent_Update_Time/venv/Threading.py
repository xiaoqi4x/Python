import threading
from Check_TC_MTBF_Recent_update_Time import Outputer
outputer1 = Outputer()
thread1 = threading.Thread(target=outputer1.result_outputer('MSIM'))
thread2 = threading.Thread(target=outputer1.result_outputer('MSIM'))
thread1.start()
thread2.start()
# thread1.join()



